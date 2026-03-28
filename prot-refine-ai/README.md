# Prot-Refine AI

A web-based protein engineering platform that allows users to perform point mutations on protein structures with real-time stability analysis and safety checks.

## Features

- **Point Mutation Analysis**: Perform single amino acid substitutions on protein structures
- **Stability Prediction**: Calculate thermodynamic stability changes using hydrophobicity scales
- **Safety Screening**: Check for potentially toxic motifs in mutated sequences
- **3D Structure Visualization**: Interactive 3D visualization of protein structures with mutation highlights
- **PDB/CIF Support**: Works with both PDB and mmCIF file formats
- **Real-time API**: FastAPI backend for instant mutation analysis
- **Modern UI**: React-based frontend with intuitive interface

## Architecture

### Backend (FastAPI)
- **api.py**: Main API server with mutation endpoints
- **main.py**: Core mutation logic using BioPython
- **requirements.txt**: Python dependencies

### Frontend (React + Vite)
- **src/App.jsx**: Main application component with 3D viewer
- **src/main.jsx**: Application entry point
- **package.json**: Node.js dependencies including 3D libraries

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Installation

1. **Clone and setup backend:**
   ```bash
   cd prot-refine-ai/backend
   pip install -r requirements.txt
   ```

2. **Setup frontend:**
   ```bash
   cd prot-refine-ai/frontend
   npm install
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   cd prot-refine-ai/backend
   uvicorn api:app --reload
   ```
   Backend will be available at `http://localhost:8000`

2. **Start the frontend:**
   ```bash
   cd prot-refine-ai/frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

## API Usage

### Mutation Endpoint

**GET** `/mutate?prompt=<mutation_prompt>`

#### Example Prompts
```
mutate GLY10 to ALA in chain A
change residue 15 to VAL in chain A
substitute HIS25 with ARG on 1Q4A chain A
```

#### Response Format
```json
{
  "mutation": "GLY10 -> ALA",
  "stability_impact": 2.2,
  "safety": "✅ Mutation likely maintains structural integrity.",
  "file": "mutated_10_ALA.pdb",
  "pdb_id": "SAMPLE",
  "res_id": 10,
  "chain_id": "A"
}
```

## 3D Visualization

The frontend includes interactive 3D protein structure visualization with the following capabilities:

- **Structure Display**: Render protein structures in 3D space
- **Mutation Highlighting**: Visual indicators for mutated residues
- **Interactive Controls**: Rotate, zoom, and pan the 3D view
- **Chain Selection**: View specific protein chains
- **Residue Details**: Hover to see residue information
- **Export Options**: Save visualization snapshots

### 3D Controls
- **Mouse**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click**: Pan view
- **Double-click**: Center on residue

## Mutation Examples

### Basic Mutations
- `mutate GLY10 to ALA in chain A` - Glycine to Alanine
- `change residue 10 to VAL in chain A` - Any residue to Valine
- `substitute GLY10 with LEU on chain A` - Glycine to Leucine

### With PDB IDs
- `mutate GLY10 to ALA in 1CRN chain A` - Uses PDB 1CRN
- `change residue 15 to VAL in 1Q4A chain A` - Uses local 1Q4A

### 3D Visualization Features
After performing a mutation, the 3D viewer will:
- Display the original protein structure
- Highlight the mutated residue in a different color
- Show stability impact indicators
- Allow interactive exploration of the structure
- Provide residue information on hover

### Stability Impact Scale
- **Positive values**: Stabilizing mutations
- **Negative values**: Destabilizing mutations
- **±2.0 threshold**: Warning for significant changes

## Safety Checks

The system automatically screens for:
- **Toxic motifs**: RGD, DTY, VGVAPG sequences
- **Stability warnings**: Large destabilizing changes
- **Aggregation risks**: High hydrophobicity increases

## File Structure

```
prot-refine-ai/
├── backend/
│   ├── api.py              # FastAPI server
│   ├── main.py             # Mutation logic
│   ├── requirements.txt    # Python deps
│   ├── data/               # Protein files
│   └── exports/            # Mutated outputs
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node deps
│   └── vite.config.js      # Vite config
└── README.md
```

## Development

### Backend Testing
```bash
cd prot-refine-ai/backend
python main.py  # Local test
```

### API Testing
```bash
# Test mutation endpoint
curl "http://localhost:8000/mutate?prompt=mutate%20GLY10%20to%20ALA%20in%20chain%20A"
```

### Frontend Development
```bash
cd prot-refine-ai/frontend
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview build
```

## Dependencies

### Backend
- **BioPython**: Protein structure parsing
- **FastAPI**: Web API framework
- **Uvicorn**: ASGI server
- **NumPy**: Numerical computations

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Three.js/React Three Fiber**: 3D visualization
- **3Dmol.js or NGL Viewer**: Molecular structure rendering

## Troubleshooting

### Backend Issues
- **File not found**: Ensure `sample.pdb` is in `backend/data/`
- **Parser errors**: Check if file is valid PDB/CIF format
- **Port conflicts**: Change uvicorn port with `--port 8001`

### Frontend Issues
- **CORS errors**: Backend must allow frontend origin
- **API connection**: Ensure backend is running on correct port
- **Build errors**: Clear node_modules and reinstall

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details
