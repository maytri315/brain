import React, { useState, useEffect, useRef } from 'react';
import * as NGL from 'ngl';

const ProteinDashboard = () => {
  const [result, setResult] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [structureData, setStructureData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const viewerRef = useRef(null);
  const stageRef = useRef(null);

  // Initialize NGL Viewer
  useEffect(() => {
    if (viewerRef.current && !stageRef.current) {
      stageRef.current = new NGL.Stage(viewerRef.current, {
        backgroundColor: '#1e293b'
      });
    }

    return () => {
      if (stageRef.current) {
        stageRef.current.dispose();
        stageRef.current = null;
      }
    };
  }, []);

  // Load and display protein structure
  const loadStructure = async (pdbData, mutationInfo = null) => {
    if (!stageRef.current) return;

    try {
      // Clear previous structures
      stageRef.current.removeAllComponents();

      // Load structure from string data
      const blob = new Blob([pdbData], { type: 'text/plain' });
      const component = await stageRef.current.loadFile(blob, { ext: 'pdb' });

      // Add cartoon representation
      component.addRepresentation('cartoon', {
        colorScheme: 'chainid',
        opacity: 0.8
      });

      // Add ball+stick for better detail
      component.addRepresentation('ball+stick', {
        sele: 'all',
        scale: 0.3,
        opacity: 0.6
      });

      // Highlight mutation if provided
      if (mutationInfo && mutationInfo.res_id) {
        const mutationSele = `${mutationInfo.res_id}`;
        component.addRepresentation('ball+stick', {
          sele: mutationSele,
          color: '#ef4444', // Red for mutation
          scale: 0.5,
          opacity: 1.0
        });

        // Add label for mutation
        component.addRepresentation('label', {
          sele: mutationSele,
          labelType: 'resname',
          color: '#ffffff',
          fontSize: 2.0,
          attachment: 'middle-center'
        });
      }

      // Auto-view the structure
      stageRef.current.autoView();

    } catch (error) {
      console.error('Error loading structure:', error);
    }
  };

  // Load initial sample structure
  useEffect(() => {
    const loadInitialStructure = async () => {
      try {
        console.log('Loading initial structure...');
        const response = await fetch('http://localhost:8000/mutate?prompt=mutate%20GLY10%20to%20GLY%20in%20chain%20A');
        console.log('Initial response status:', response.status);
        const data = await response.json();
        console.log('Initial data:', data);

        if (data && data.file) {
          // Load the exported PDB file
          console.log('Loading initial file:', data.file);
          const pdbResponse = await fetch(`http://localhost:8000/exports/${data.file}`);
          console.log('Initial PDB response status:', pdbResponse.status);
          if (pdbResponse.ok) {
            const pdbData = await pdbResponse.text();
            console.log('Initial PDB data length:', pdbData.length);
            setStructureData(pdbData);
            loadStructure(pdbData);
          } else {
            console.error('Could not load initial PDB file');
          }
        } else {
          console.warn('No file in initial response, using sample data');
          // Load sample.pdb directly
          const sampleResponse = await fetch('http://localhost:8000/exports/sample.pdb');
          console.log('Sample response status:', sampleResponse.status);
          if (sampleResponse.ok) {
            const pdbData = await sampleResponse.text();
            console.log('Sample PDB data length:', pdbData.length);
            setStructureData(pdbData);
            loadStructure(pdbData);
          } else {
            console.error('Could not load sample structure');
          }
        }
      } catch (error) {
        console.error('Error loading initial structure:', error);
      }
    };

    if (stageRef.current) {
      loadInitialStructure();
    }
  }, []);

  const handleMutation = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`http://localhost:8000/mutate?prompt=${encodeURIComponent(prompt)}`);
      const data = await response.json();

      if (data.error) {
        setError(data.error);
        return;
      }

      setResult(data);

      if (data.file) {
        // Load the mutated structure
        console.log('Loading file:', data.file);
        const pdbResponse = await fetch(`http://localhost:8000/exports/${data.file}`);
        console.log('PDB response status:', pdbResponse.status);
        if (pdbResponse.ok) {
          const pdbData = await pdbResponse.text();
          console.log('PDB data length:', pdbData.length);
          setStructureData(pdbData);
          loadStructure(pdbData, data);
        } else {
          console.error('Failed to load PDB file:', pdbResponse.status, pdbResponse.statusText);
          setError('Failed to load 3D structure');
        }
      } else {
        // Mutation successful but no file, keep current structure
        console.log('Mutation completed without file generation');
      }
    } catch (error) {
      console.error('Mutation error:', error);
      setError('Failed to perform mutation. Please check your prompt and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <h1 className="text-3xl font-bold text-cyan-400 mb-6">ProtRefine AI Engine</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Input Section */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <label className="block mb-2 text-sm font-medium">Mutation Prompt</label>
          <input
            className="w-full p-3 rounded bg-slate-700 border-none focus:ring-2 focus:ring-cyan-500 text-white placeholder-slate-400"
            placeholder="e.g., GLY10 to ALA, mutate GLY to ALA, or just 'ALA'"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <div className="mt-2 text-xs text-slate-400">
            Examples: "GLY10 to ALA", "mutate GLY to VAL", "from ASP to GLU", "GLY → ALA"
          </div>
          <button
            onClick={handleMutation}
            className="mt-4 w-full bg-cyan-600 hover:bg-cyan-500 p-3 rounded font-bold transition disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!prompt.trim()}
          >
            Execute Mutation
          </button>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4 text-cyan-300">Analysis Results</h2>
            <div className="space-y-4">
              {result.error ? (
                <div className="text-red-400 p-3 bg-red-900/20 rounded">
                  Error: {result.error}
                </div>
              ) : (
                <>
                  <div className="flex justify-between border-b border-slate-700 pb-2">
                    <span>Mutation:</span> <span className="font-mono text-yellow-400">{result.mutation}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-700 pb-2">
                    <span>Stability Impact:</span>
                    <span className={result.stability_impact > 0 ? "text-green-400" : result.stability_impact < -2 ? "text-red-400" : "text-yellow-400"}>
                      {result.stability_impact} ΔΔG
                    </span>
                  </div>
                  <div className="p-3 bg-slate-900 rounded text-sm italic text-slate-300">
                    {result.safety}
                  </div>
                  {result.file && (
                    <div className="text-xs text-slate-400">
                      File: {result.file}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 3D Viewer Section */}
      <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h2 className="text-xl font-semibold mb-4 text-cyan-300">3D Protein Structure</h2>
        <div
          ref={viewerRef}
          className="w-full h-96 bg-slate-900 rounded border border-slate-600"
          style={{ minHeight: '400px' }}
        />
        <div className="mt-4 text-sm text-slate-400">
          <p><strong>Controls:</strong> Mouse to rotate • Scroll to zoom • Right-click to pan</p>
          {result && !result.error && (
            <p className="text-cyan-400 mt-2">🔴 Red highlight shows the mutated residue</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProteinDashboard;