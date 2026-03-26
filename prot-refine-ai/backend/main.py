from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import PDBIO
import os

# Thermodynamic stability scale (approximate ΔG values)
# Positive values generally indicate increased hydrophobic stability
STABILITY_SCALE = {
    "ALA": 1.8, "CYS": 2.5, "ASP": -3.5, "GLU": -3.5, "PHE": 2.8,
    "GLY": -0.4, "HIS": -3.2, "ILE": 4.5, "LYS": -3.9, "LEU": 3.8,
    "MET": 1.9, "ASN": -3.5, "PRO": -1.6, "GLN": -3.5, "ARG": -4.5,
    "SER": -0.8, "THR": -0.7, "VAL": 4.2, "TRP": -0.9, "TYR": -1.3
}

def run_mutation(pdb_path, chain_id, res_num, target_amino):
    """
    Performs a point mutation on a protein structure and calculates stability impact.
    """
    try:
        # 1. Determine file type and parse
        if pdb_path.endswith('.cif'):
            parser = MMCIFParser(QUIET=True)
        else:
            parser = PDBParser(QUIET=True)
        
        if not os.path.exists(pdb_path):
            return {"error": f"File not found at {pdb_path}"}

        structure = parser.get_structure('protein', pdb_path)
        model = structure[0]
        chain = model[chain_id]
        
        # 2. Locate residue and identify original type
        residue = chain[res_num]
        original_amino = residue.get_resname()
        
        # 3. Apply Mutation (Rename the residue)
        target_amino = target_amino.upper()
        residue.resname = target_amino
        
        # 4. Calculate Stability Delta (ΔΔG approximation)
        # Formula: Stability(Target) - Stability(Original)
        orig_val = STABILITY_SCALE.get(original_amino, 0)
        target_val = STABILITY_SCALE.get(target_amino, 0)
        stability_delta = round(target_val - orig_val, 2)
        
        # 5. Safety Logic
        safety_status = "✅ Mutation likely maintains structural integrity."
        if stability_delta < -2.0:
            safety_status = "⚠️ Warning: Significant decrease in stability detected."
        elif stability_delta > 3.0:
            safety_status = "ℹ️ Notice: High hydrophobicity increase; monitor for aggregation."

        # 6. Export Mutated File
        export_filename = f"mutated_{res_num}_{target_amino}.pdb"
        export_path = os.path.join("exports", export_filename)
        
        # Create exports folder if it doesn't exist
        if not os.path.exists("exports"):
            os.makedirs("exports")
            
        io = PDBIO()
        io.set_structure(structure)
        io.save(export_path)

        return {
            "mutation": f"{original_amino}{res_num} -> {target_amino}",
            "stability_impact": stability_delta,
            "safety": safety_status,
            "file": export_filename
        }

    except Exception as e:
        return {"error": str(e), "safety": "❌ System failure during mutagenesis."}

if __name__ == "__main__":
    # Test block for local execution
    print("Running local test...")
    test_result = run_mutation("data/sample.pdb", "A", 10, "ALA")
    print(test_result)