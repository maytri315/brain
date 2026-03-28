from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    """
    Flexible parsing for protein mutation prompts.
    Supports various formats like:
    - "mutate GLY10 to ALA"
    - "change glycine 10 to alanine"
    - "GLY10 -> ALA"
    - "substitute residue 10 with ALA"
    """
    p = prompt.upper()

    # 1. Look for a 4-character PDB ID (e.g., 1CRN, 6LU7)
    pdb_match = re.search(r'\b([0-9][A-Z0-9]{3})\b', p)
    pdb_id = pdb_match.group(1) if pdb_match else "SAMPLE"

    # 2. Look for Chain (e.g., "Chain A", "chain B", "A", "B")
    chain_match = re.search(r'(?:chain|CHAIN)\s*([A-Z])|(\b[A-Z]\b)(?!\w)', p)
    chain_id = (chain_match.group(1) or chain_match.group(2)) if chain_match else "A"

    # 3. Look for Residue Number (more flexible)
    res_match = re.search(r'(?:residue|RESIDUE)?\s*(\d+)', p)
    if not res_match:
        # Look for number after amino acid abbreviations
        res_match = re.search(r'(?:GLY|ALA|CYS|ASP|GLU|PHE|HIS|ILE|LYS|LEU|MET|ASN|PRO|GLN|ARG|SER|THR|VAL|TRP|TYR)\s*(\d+)', p)
    res_id = int(res_match.group(1)) if res_match else 10

    # 4. Look for Amino Acids - improved logic
    amino_acids = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR']

    # First, try to find amino acids after mutation keywords
    target_amino = None
    source_amino = None

    # Look for patterns like "GLY10 to ALA" or "from GLY to ALA"
    mutation_patterns = [
        r'(\w{3})\d*\s*(?:to|->|into|with)\s*(\w{3})',  # GLY to ALA
        r'(?:from|change)\s*(\w{3})\s*(?:to|into)\s*(\w{3})',  # from GLY to ALA
        r'(\w{3})\d*\s*->\s*(\w{3})',  # GLY10 -> ALA
        r'substitute\s*(\w{3})\d*\s*(?:with|to)\s*(\w{3})',  # substitute GLY with ALA
    ]

    for pattern in mutation_patterns:
        match = re.search(pattern, p, re.IGNORECASE)
        if match:
            source_amino = match.group(1).upper()
            target_amino = match.group(2).upper()
            break

    # If no mutation pattern found, look for any amino acids
    if not target_amino:
        amino_matches = re.findall(r'\b(' + '|'.join(amino_acids) + r')\b', p)
        if len(amino_matches) >= 2:
            # Assume first is source, last is target
            source_amino = amino_matches[0]
            target_amino = amino_matches[-1]
        elif len(amino_matches) == 1:
            target_amino = amino_matches[0]

    # Validate amino acids
    if target_amino and target_amino not in amino_acids:
        target_amino = "ALA"  # Default fallback

    target_amino = target_amino or "ALA"

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

@app.get("/exports/{filename}")
async def get_exported_file(filename: str):
    """Serve exported PDB files for 3D visualization."""
    file_path = os.path.join("exports", filename)
    if not os.path.exists(file_path):
        # Try data directory as fallback
        file_path = os.path.join("data", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='chemical/x-pdb', filename=filename)