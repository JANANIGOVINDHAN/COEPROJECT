import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, LayoutDashboard, TriangleAlert, Cpu, 
  Wrench, ShieldCheck, FileText, RefreshCw, Eye, Download, 
  CheckCircle, Search, Filter, AlertOctagon, TrendingUp
} from 'lucide-react';
import { 
  getDashboardSummary, getDashboardTrends, getDriftFindings, 
  triggerDriftScan, generatePDFReport 
} from './services/api';
import { DiffViewerModal } from './components/DiffViewerModal';
import { MLSentinelView } from './components/MLSentinelView';
import { RemediationConsole } from './components/RemediationConsole';
import { ComplianceTicketsView } from './components/ComplianceTicketsView';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [summary, setSummary] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);
  const [findings, setFindings] = useState<any[]>([]);
  const [selectedFinding, setSelectedFinding] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [severityFilter, setSeverityFilter] = useState<string>('');
  const [scanning, setScanning] = useState<boolean>(false);
  const [reportDownloading, setReportDownloading] = useState<boolean>(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [s, t, f] = await Promise.all([
        getDashboardSummary(),
        getDashboardTrends(),
        getDriftFindings()
      ]);
      setSummary(s);
      setTrends(t);
      setFindings(f);
    } catch (e) {
      console.error(e);
    }
  };

  const handleScan = async () => {
    try {
      setScanning(true);
      await triggerDriftScan();
      await loadData();
      alert('Full network configuration drift scan completed successfully!');
    } catch (e: any) {
      alert('Scan error: ' + e.message);
    } finally {
      setScanning(false);
    }
  };

  const handleGeneratePDF = async () => {
    try {
      setReportDownloading(true);
      const res = await generatePDFReport();
      alert(`PDF Audit Report generated successfully: ${res.report_path || res.filename || 'ReportLab PDF'}`);
    } catch (e: any) {
      alert('PDF generation error: ' + e.message);
    } finally {
      setReportDownloading(false);
    }
  };

  const filteredFindings = findings.filter(f => {
    const matchesSearch = !searchQuery || 
      f.hostname.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.field_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.finding_id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSeverity = !severityFilter || f.severity === severityFilter;
    return matchesSearch && matchesSeverity;
  });

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800/80 p-4 flex flex-col justify-between select-none">
        <div>
          {/* Logo & Header */}
          <div className="flex items-center space-x-3 mb-8 px-2">
            <div className="p-2.5 bg-cyan-500/20 text-cyan-400 rounded-xl border border-cyan-500/30">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-sm text-slate-100 tracking-wide">DRIFT SENTINEL</h1>
              <p className="text-[11px] text-cyan-400 font-medium">Hospital NetSec • Phase 2</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1.5">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                activeTab === 'dashboard' 
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm' 
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </button>

            <button 
              onClick={() => setActiveTab('findings')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                activeTab === 'findings' 
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm' 
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <TriangleAlert className="w-4 h-4" />
              <span>Drift Findings</span>
              {summary?.kpis?.total_findings > 0 && (
                <span className="ml-auto px-2 py-0.5 bg-red-500/20 text-red-400 rounded-full text-[10px] font-mono font-bold">
                  {summary.kpis.total_findings}
                </span>
              )}
            </button>

            <button 
              onClick={() => setActiveTab('remediation')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                activeTab === 'remediation' 
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm' 
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <Wrench className="w-4 h-4" />
              <span>Remediation Console</span>
            </button>

            <button 
              onClick={() => setActiveTab('ml_sentinel')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                activeTab === 'ml_sentinel' 
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm' 
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>ML Sentinel Engine</span>
            </button>

            <button 
              onClick={() => setActiveTab('compliance')}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                activeTab === 'compliance' 
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm' 
                  : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Compliance & Tickets</span>
            </button>
          </nav>
        </div>

        {/* User Card */}
        <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold text-slate-200">Dr. Sarah Jenkins</p>
            <p className="text-[10px] font-mono text-cyan-400">Chief Security Officer</p>
          </div>
          <span className="w-2.5 h-2.5 bg-emerald-400 rounded-full animate-pulse"></span>
        </div>
      </aside>

      {/* Main Container */}
      <main className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-950">
        {/* Header Actions */}
        <header className="flex justify-between items-center pb-4 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              Hospital Network Configuration Drift Sentinel
            </h2>
            <p className="text-xs text-slate-400">Multi-Site Enterprise NetSec Monitoring & Compliance Automation Platform</p>
          </div>

          <div className="flex items-center space-x-3">
            <button 
              onClick={handleGeneratePDF}
              disabled={reportDownloading}
              className="bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold px-3.5 py-2 rounded-xl text-xs flex items-center space-x-2 transition"
            >
              <FileText className="w-4 h-4 text-cyan-400" />
              <span>{reportDownloading ? 'Generating PDF...' : 'Download PDF Report'}</span>
            </button>

            <button 
              onClick={handleScan}
              disabled={scanning}
              className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-slate-800 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs flex items-center space-x-2 transition shadow-lg shadow-cyan-500/20"
            >
              <RefreshCw className={`w-4 h-4 ${scanning ? 'animate-spin' : ''}`} />
              <span>{scanning ? 'Scanning...' : 'Run Network Drift Scan'}</span>
            </button>
          </div>
        </header>

        {/* View 1: Main Dashboard */}
        {activeTab === 'dashboard' && summary && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p className="text-xs text-slate-400 font-medium">Hospital Sites</p>
                <h3 className="text-3xl font-mono font-bold text-slate-100 mt-2">{summary.kpis.total_sites}</h3>
                <p className="text-[11px] text-slate-500 mt-1">113 Network Devices Scanned</p>
              </div>

              <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p className="text-xs text-slate-400 font-medium">Active Drift Findings</p>
                <h3 className="text-3xl font-mono font-bold text-amber-400 mt-2">{summary.kpis.total_findings}</h3>
                <p className="text-[11px] text-slate-500 mt-1">Requiring Review</p>
              </div>

              <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p className="text-xs text-slate-400 font-medium">Critical Mismatches</p>
                <h3 className="text-3xl font-mono font-bold text-red-400 mt-2">{summary.kpis.critical_findings}</h3>
                <p className="text-[11px] text-slate-500 mt-1">High Blast Radius</p>
              </div>

              <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                <p className="text-xs text-slate-400 font-medium">Unauthorized Changes</p>
                <h3 className="text-3xl font-mono font-bold text-red-500 mt-2">{summary.kpis.unauthorized_changes}</h3>
                <p className="text-[11px] text-slate-500 mt-1">No Valid CAB Ticket</p>
              </div>
            </div>

            {/* Middle Section: Site Risk Matrix & Top Risky Devices */}
            <div className="grid grid-cols-3 gap-6">
              {/* Site Risk Matrix Table */}
              <div className="col-span-2 bg-slate-900 rounded-2xl border border-slate-800 p-5">
                <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-cyan-400" />
                    Multi-Site Vulnerability Matrix
                  </span>
                  {trends && (
                    <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-lg border border-cyan-500/20">
                      MTTR: {trends.metrics?.mttr_hours} hrs
                    </span>
                  )}
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-sans">
                    <thead className="text-slate-400 border-b border-slate-800 font-mono">
                      <tr>
                        <th className="p-2">Site Name</th>
                        <th className="p-2">Criticality</th>
                        <th className="p-2">Devices</th>
                        <th className="p-2">Drift Count</th>
                        <th className="p-2">Avg Risk Score</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/80">
                      {trends?.site_risk_matrix?.map((s: any) => (
                        <tr key={s.site_id} className="hover:bg-slate-800/30 transition">
                          <td className="p-2 font-bold text-slate-200">{s.site_name}</td>
                          <td className="p-2 font-mono text-amber-400 font-semibold">{s.criticality}</td>
                          <td className="p-2 font-mono text-slate-400">{s.device_count}</td>
                          <td className="p-2 font-mono font-bold text-cyan-400">{s.active_findings}</td>
                          <td className="p-2 font-mono font-bold text-red-400">{s.average_risk_score}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Top Risky Devices */}
              <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5">
                <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center gap-2">
                  <AlertOctagon className="w-4 h-4 text-red-400" />
                  Top Risky Devices
                </h3>
                <div className="space-y-3">
                  {summary.charts.top_risky_devices.map((d: any) => (
                    <div key={d.device_id} className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                      <div>
                        <p className="font-bold text-slate-200">{d.hostname}</p>
                        <p className="font-mono text-[10px] text-slate-500">{d.device_id}</p>
                      </div>
                      <span className="px-2.5 py-1 bg-red-500/20 text-red-400 font-mono font-bold rounded-lg text-xs border border-red-500/30">
                        {d.risk_score}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* View 2: Drift Findings Grid & Diff Viewer */}
        {activeTab === 'findings' && (
          <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5 space-y-4">
            {/* Filter Bar */}
            <div className="flex justify-between items-center gap-4">
              <div className="relative flex-1">
                <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search by hostname, field name, or finding ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-slate-400" />
                <select
                  value={severityFilter}
                  onChange={(e) => setSeverityFilter(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
                >
                  <option value="">All Severities</option>
                  <option value="CRITICAL">CRITICAL</option>
                  <option value="HIGH">HIGH</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="LOW">LOW</option>
                </select>
              </div>
            </div>

            {/* Findings Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="text-slate-400 border-b border-slate-800 font-mono">
                  <tr>
                    <th className="p-3">ID</th>
                    <th className="p-3">Hostname</th>
                    <th className="p-3">Target Field</th>
                    <th className="p-3">Severity</th>
                    <th className="p-3">Authorization</th>
                    <th className="p-3">Risk Score</th>
                    <th className="p-3">Status</th>
                    <th className="p-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80">
                  {filteredFindings.map((f: any) => (
                    <tr key={f.finding_id} className="hover:bg-slate-800/30 transition">
                      <td className="p-3 font-mono text-cyan-400 font-bold">{f.finding_id}</td>
                      <td className="p-3 font-bold text-slate-200">{f.hostname}</td>
                      <td className="p-3 font-mono text-amber-400">{f.field_name}</td>
                      <td className="p-3 font-bold">
                        <span className={`px-2 py-0.5 rounded text-[10px] ${
                          f.severity === 'CRITICAL' ? 'bg-red-500/20 text-red-400' :
                          f.severity === 'HIGH' ? 'bg-orange-500/20 text-orange-400' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {f.severity}
                        </span>
                      </td>
                      <td className="p-3 font-medium">
                        <span className={`px-2 py-0.5 rounded text-[10px] ${
                          f.authorization_status === 'Authorized' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                        }`}>
                          {f.authorization_status}
                        </span>
                      </td>
                      <td className="p-3 font-mono font-bold text-cyan-400">{f.risk_score}</td>
                      <td className="p-3 font-mono text-[11px] text-slate-400">{f.status}</td>
                      <td className="p-3 text-right">
                        <button
                          onClick={() => setSelectedFinding(f)}
                          className="px-3 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-lg text-xs font-semibold flex items-center space-x-1.5 ml-auto transition"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>View Diff</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* View 3: Remediation Console */}
        {activeTab === 'remediation' && <RemediationConsole />}

        {/* View 4: Machine Learning Sentinel View */}
        {activeTab === 'ml_sentinel' && <MLSentinelView />}

        {/* View 5: Compliance & CAB Tickets */}
        {activeTab === 'compliance' && <ComplianceTicketsView />}
      </main>

      {/* Diff Viewer Modal */}
      {selectedFinding && (
        <DiffViewerModal
          finding={selectedFinding}
          onClose={() => setSelectedFinding(null)}
          onRemediate={(id) => {
            setActiveTab('remediation');
          }}
        />
      )}
    </div>
  );
}
