import os
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB import PDBIO

# 1. Physics Layer: Hydrophobicity scales for stability estimation
STABILITY_INDEX = {
    "ALA": 1.8, "ARG": -4.5, "ASN": -3.5, "ASP": -3.5, "CYS": 2.5, 
    "GLU": -3.5, "GLN": -3.5, "GLY": -0.4, "HIS": -3.2, "ILE": 4.5, 
    "LEU": 3.8, "LYS": -3.9, "MET": 1.9, "PHE": 2.8, "PRO": -1.6, 
    "SER": -0.8, "THR": -0.7, "TRP": -0.9, "TYR": -1.3, "VAL": 4.2
}

# 2. Safety Layer: Pathogenicity motifs
def safety_check(sequence):
    toxic_patterns = ["RGD", "DTY", "VGVAPG"]
    for pattern in toxic_patterns:
        if pattern in sequence:
            return f"❌ FAILED: Toxic motif {pattern} detected."
    return "✅ PASSED: No pathogenic motifs detected."

# 3. Structural Layer: The Mutagenesis Engine
def run_mutation(pdb_path, chain_id, res_num, target_amino):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('protein', pdb_path)
    
    old_res = ""
    seq_list = []
    found = False

    for model in structure:
        for chain in model:
            if chain.id == chain_id:
                for residue in chain:
                    res_name = residue.get_resname()
                    seq_list.append(res_name)
                    if residue.id[1] == res_num:
                        old_res = res_name
                        residue.resname = target_amino
                        found = True
    
    if not found:
        return f"Error: Could not find residue {res_num} in Chain {chain_id}."

    # Calculate Stability Change
    delta = STABILITY_INDEX.get(target_amino, 0) - STABILITY_INDEX.get(old_res, 0)
    safety_status = safety_check("".join(seq_list))

    # Save mutated file
    io = PDBIO()
    io.set_structure(structure)
    output_name = f"mutated_{res_num}.pdb"
    io.save(output_name)

    return {
        "mutation": f"{old_res}{res_num} -> {target_amino}{res_num}",
        "stability_impact": round(delta, 2),
        "safety": safety_status,
        "file": output_name
    }

# 4. Interface Layer: Simple NLP Parser
def nlp_interface(prompt):
    # In a full project, this would be an LLM API call.
    # Here, we simulate the extraction logic.
    print(f"\n[User Prompt]: {prompt}")
    
    # Simple keyword extraction for the demo
    words = prompt.upper().split()
    target_res = words[-1] # Assumes last word is the target amino (e.g. ALA)
    
    # For demo: assume Chain A, Position 10 based on our successful test
    result = run_mutation("c:/brain/sample.pdb", "A", 10, target_res)
    
    print("-" * 30)
    print(f"Mutation Executed: {result['mutation']}")
    print(f"Stability Delta: {result['stability_impact']}")
    print(f"Safety Status: {result['safety']}")
    print(f"File Saved: {result['file']}")

# Run the Demo
if __name__ == "__main__":
    nlp_interface("Change the 10th residue to ALA")