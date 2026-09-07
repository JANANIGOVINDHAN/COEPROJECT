import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, LayoutDashboard, TriangleAlert, Building2, 
  Network, Sliders, CheckSquare, Ticket, FileText, Activity 
} from 'lucide-react';
import { getDashboardSummary, getDriftFindings, triggerDriftScan } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [summary, setSummary] = useState<any>(null);
  const [findings, setFindings] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const s = await getDashboardSummary();
      const f = await getDriftFindings();
      setSummary(s);
      setFindings(f);
    } catch (e) {
      console.error(e);
    }
  };

  const handleScan = async () => {
    try {
      await triggerDriftScan();
      alert('Drift Scan triggered successfully');
      loadData();
    } catch (e) {
      alert('Scan error: ' + e);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-3 mb-8 px-2">
            <div className="p-2 bg-cyan-500/20 text-cyan-400 rounded-xl">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-sm">DRIFT SENTINEL</h1>
              <p className="text-xs text-cyan-400">Hospital NetSec</p>
            </div>
          </div>

          <nav className="space-y-1">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium ${activeTab === 'dashboard' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </button>
            <button 
              onClick={() => setActiveTab('findings')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium ${activeTab === 'findings' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              <TriangleAlert className="w-4 h-4" />
              <span>Drift Findings</span>
            </button>
          </nav>
        </div>

        <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50">
          <p className="text-xs font-semibold">Dr. Sarah Jenkins</p>
          <p className="text-[11px] text-cyan-400">Administrator</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        <header className="flex justify-between items-center pb-4 border-b border-slate-800">
          <h2 className="text-xl font-bold">Hospital Network Drift Sentinel</h2>
          <button 
            onClick={handleScan}
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-4 py-2 rounded-lg text-xs"
          >
            Run Drift Scan
          </button>
        </header>

        {activeTab === 'dashboard' && summary && (
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400">Total Sites</p>
              <h3 className="text-2xl font-bold">{summary.kpis.total_sites}</h3>
            </div>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400">Active Findings</p>
              <h3 className="text-2xl font-bold text-amber-400">{summary.kpis.total_findings}</h3>
            </div>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400">Critical Mismatches</p>
              <h3 className="text-2xl font-bold text-red-400">{summary.kpis.critical_findings}</h3>
            </div>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400">Unauthorized Changes</p>
              <h3 className="text-2xl font-bold text-red-400">{summary.kpis.unauthorized_changes}</h3>
            </div>
          </div>
        )}

        {activeTab === 'findings' && (
          <div className="bg-slate-900 rounded-xl border border-slate-800 p-4">
            <h3 className="font-bold text-sm mb-4">Active Configuration Drift Findings</h3>
            <table className="w-full text-left text-xs">
              <thead class="text-slate-400 border-b border-slate-800">
                <tr>
                  <th class="p-2">ID</th>
                  <th class="p-2">Hostname</th>
                  <th class="p-2">Field</th>
                  <th class="p-2">Severity</th>
                  <th class="p-2">Auth Status</th>
                  <th class="p-2">Risk</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {findings.map((f: any) => (
                  <tr key={f.finding_id}>
                    <td className="p-2 font-mono text-cyan-400">{f.finding_id}</td>
                    <td className="p-2 font-bold">{f.hostname}</td>
                    <td className="p-2 font-mono">{f.field_name}</td>
                    <td className="p-2 font-bold text-red-400">{f.severity}</td>
                    <td className="p-2">{f.authorization_status}</td>
                    <td className="p-2 font-bold">{f.risk_score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
