import React, { useState } from 'react';

const ProteinDashboard = () => {
  const [result, setResult] = useState(null);
  const [prompt, setPrompt] = useState("");

  const handleMutation = async () => {
    // Call your Python API
    const response = await fetch(`http://localhost:8000/mutate?prompt=${prompt}`);
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <h1 className="text-3xl font-bold text-cyan-400 mb-6">ProtRefine AI Engine</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <label className="block mb-2 text-sm font-medium">Mutation Prompt</label>
          <input 
            className="w-full p-3 rounded bg-slate-700 border-none focus:ring-2 focus:ring-cyan-500"
            placeholder="e.g., Change residue 10 to Alanine"
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button 
            onClick={handleMutation}
            className="mt-4 w-full bg-cyan-600 hover:bg-cyan-500 p-3 rounded font-bold transition"
          >
            Execute Mutation
          </button>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4 text-cyan-300">Analysis Results</h2>
            <div className="space-y-4">
              <div className="flex justify-between border-b border-slate-700 pb-2">
                <span>Mutation:</span> <span className="font-mono text-yellow-400">{result.mutation}</span>
              </div>
              <div className="flex justify-between border-b border-slate-700 pb-2">
                <span>Stability Impact:</span> 
                <span className={result.stability_impact > 0 ? "text-green-400" : "text-red-400"}>
                  {result.stability_impact} ΔΔG
                </span>
              </div>
              <div className="p-3 bg-slate-900 rounded text-sm italic text-slate-300">
                {result.safety}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProteinDashboard;