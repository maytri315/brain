from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import main  # This imports the logic we built in Part 2

app = FastAPI()

# Allow your React app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/mutate")
async def mutate_endpoint(prompt: str, chain: str = "A", res_id: int = 10):
    # This simulates the NLP extraction and runs your engine
    target_amino = "ALA" if "ALA" in prompt.upper() else "GLY"
    result = main.run_mutation("c:/brain/sample.pdb", chain, res_id, target_amino)
    return result

# To run: pip install fastapi uvicorn
# Command: uvicorn api:app --reload