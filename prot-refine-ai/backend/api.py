from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import main
import re
import os
import urllib.request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

def get_pdb_file(pdb_id):
    """Downloads PDB from RCSB if not already in data/ folder."""
    pdb_id = pdb_id.upper()
    file_path = f"data/{pdb_id}.pdb"
    if not os.path.exists(file_path):
        try:
            url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
            urllib.request.urlretrieve(url, file_path)
        except:
            return "data/sample.pdb" # Fallback to sample if download fails
    return file_path

def parse_protein_prompt(prompt: str):
    p = prompt.upper()
    
    # 1. Look for a 4-character PDB ID (e.g., 1CRN, 6LU7)
    pdb_match = re.search(r'\b([0-9][A-Z0-9]{3})\b', p)
    pdb_id = pdb_match.group(1) if pdb_match else "SAMPLE"
    
    # 2. Look for Chain (e.g., "Chain A", "Chain B")
    chain_match = re.search(r'CHAIN\s*([A-Z])', p)
    chain_id = chain_match.group(1) if chain_match else "A"

    # 3. Look for Residue Number
    res_match = re.search(r'(\d+)', p)
    res_id = int(res_match.group(1)) if res_match else 10
    
    # 4. Look for Amino Acid
    amino_match = re.search(r'(ALA|CYS|ASP|GLU|PHE|GLY|HIS|ILE|LYS|LEU|MET|ASN|PRO|GLN|ARG|SER|THR|VAL|TRP|TYR)', p)
    target_amino = amino_match.group(1) if amino_match else "ALA"
    
    return pdb_id, chain_id, res_id, target_amino

@app.get("/mutate")
async def mutate_endpoint(prompt: str):
    # Dynamic parsing
    pdb_id, chain_id, res_id, target_amino = parse_protein_prompt(prompt)
    
    # Get the file path (either local or downloaded)
    file_path = get_pdb_file(pdb_id)
    
    # Run mutation
    result = main.run_mutation(file_path, chain_id, res_id, target_amino)
    
    # Add extra info for React to use
    result["pdb_id"] = pdb_id
    result["res_id"] = res_id
    result["chain_id"] = chain_id
    
    return result