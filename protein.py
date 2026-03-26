from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB import PDBIO

# Simple hydrophobicity scale for stability estimation
HYDRO_SCALE = {"ALA": 1.8, "ARG": -4.5, "ASN": -3.5, "ASP": -3.5, "CYS": 2.5, "GLU": -3.5, "GLN": -3.5, "GLY": -0.4, "HIS": -3.2, "ILE": 4.5, "LEU": 3.8, "LYS": -3.9, "MET": 1.9, "PHE": 2.8, "PRO": -1.6, "SER": -0.8, "THR": -0.7, "TRP": -0.9, "TYR": -1.3, "VAL": 4.2}

def check_safety(sequence):
    # Search for bio-active motifs that could be toxic
    toxic_motifs = ["RGD", "DTY", "VGVAPG"] 
    for motif in toxic_motifs:
        if motif in sequence:
            return f"⚠️ WARNING: Toxic Motif '{motif}' detected!"
    return "✅ Safety Check Passed."

def mutate_and_analyze(pdb_file, chain_id, res_id, new_res):
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure('prot', pdb_file)
    
    old_res_name = ""
    full_sequence = ""

    for model in structure:
        for chain in model:
            if chain.id == chain_id:
                for residue in chain:
                    res_name = residue.get_resname()
                    full_sequence += res_name
                    if residue.id[1] == res_id:
                        old_res_name = res_name
                        residue.resname = new_res # Perform mutation

    if not old_res_name:
        print("Error: Residue not found.")
        return

    # 1. Stability Logic (Simplified Delta Hydrophobicity)
    stability_delta = HYDRO_SCALE.get(new_res, 0) - HYDRO_SCALE.get(old_res_name, 0)
    stability_msg = "Stabilizing" if stability_delta > 0 else "Potential Destabilizing"

    # 2. Save and Report
    io = PDBIO()
    io.set_structure(structure)
    io.save("mutated_protein.pdb")

    print(f"\n--- Analysis for {old_res_name}{res_id} -> {new_res}{res_id} ---")
    print(f"Stability Impact: {stability_delta:.2f} ({stability_msg})")
    print(check_safety(full_sequence))
    print(f"Result saved to 'mutated_protein.pdb'")

# Test it
mutate_and_analyze("c:/brain/sample.pdb", "A", 10, "ALA")