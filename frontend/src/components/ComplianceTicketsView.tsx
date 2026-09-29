import React, { useState, useEffect } from 'react';
import { ShieldCheck, Ticket, CheckCircle2, AlertTriangle, FileText } from 'lucide-react';
import { getComplianceRules, getChangeTickets } from '../services/api';

export const ComplianceTicketsView: React.FC = () => {
  const [rules, setRules] = useState<any[]>([]);
  const [tickets, setTickets] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'rules' | 'tickets'>('rules');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rData, tData] = await Promise.all([
        getComplianceRules(),
        getChangeTickets()
      ]);
      setRules(rData);
      setTickets(tData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-slate-400 font-mono text-center">Loading Compliance & Ticket Matrix...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-cyan-500/20 text-cyan-400 rounded-2xl border border-cyan-500/30">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              Compliance Rules & CAB Ticket Registry
              <span className="px-2.5 py-0.5 text-[10px] font-mono font-semibold bg-cyan-500/20 text-cyan-400 rounded-full border border-cyan-500/30">
                Phase 2 Integrated
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              31 Security Policies (HIPAA / NIST) & CAB Ticket Window Validation Engine
            </p>
          </div>
        </div>

        {/* Tab Toggle Buttons */}
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
          <button
            onClick={() => setActiveTab('rules')}
            className={`px-4 py-2 rounded-lg font-bold transition flex items-center space-x-2 ${
              activeTab === 'rules' ? 'bg-cyan-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Compliance Rules ({rules.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('tickets')}
            className={`px-4 py-2 rounded-lg font-bold transition flex items-center space-x-2 ${
              activeTab === 'tickets' ? 'bg-cyan-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Ticket className="w-4 h-4" />
            <span>CAB Tickets ({tickets.length})</span>
          </button>
        </div>
      </div>

      {/* Rules Table */}
      {activeTab === 'rules' && (
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5">
          <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Database-Backed Security Compliance Policies
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800 font-mono">
                <tr>
                  <th className="p-3">Rule ID</th>
                  <th className="p-3">Rule Name</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Target Field</th>
                  <th className="p-3">Required Standard</th>
                  <th className="p-3">Severity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80">
                {rules.map((r: any) => (
                  <tr key={r.rule_id} className="hover:bg-slate-800/40 transition">
                    <td className="p-3 font-mono text-cyan-400 font-bold">{r.rule_id}</td>
                    <td className="p-3 font-semibold text-slate-200">{r.rule_name}</td>
                    <td className="p-3 text-slate-400">{r.category}</td>
                    <td className="p-3 font-mono text-amber-400">{r.target_field}</td>
                    <td className="p-3 font-mono text-emerald-400">{r.expected_value}</td>
                    <td className="p-3 font-bold text-red-400">{r.severity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tickets Table */}
      {activeTab === 'tickets' && (
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5">
          <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center gap-2">
            <Ticket className="w-4 h-4 text-cyan-400" />
            Change Advisory Board (CAB) Ticket Registry
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800 font-mono">
                <tr>
                  <th className="p-3">Ticket ID</th>
                  <th className="p-3">Site ID</th>
                  <th className="p-3">Device ID</th>
                  <th className="p-3">Title</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Approved Window</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80">
                {tickets.slice(0, 50).map((t: any) => (
                  <tr key={t.ticket_id} className="hover:bg-slate-800/40 transition">
                    <td className="p-3 font-mono text-cyan-400 font-bold">{t.ticket_id}</td>
                    <td className="p-3 font-mono text-slate-300">{t.site_id}</td>
                    <td className="p-3 font-mono text-slate-300">{t.device_id || 'ALL'}</td>
                    <td className="p-3 text-slate-200 font-medium">{t.title}</td>
                    <td className="p-3 font-bold">
                      <span className={`px-2 py-0.5 rounded text-[10px] ${
                        t.approval_status === 'Approved' ? 'bg-emerald-500/20 text-emerald-400' :
                        t.approval_status === 'Expired' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                      }`}>
                        {t.approval_status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-400 text-[11px]">
                      {t.start_time?.slice(0, 16)} to {t.end_time?.slice(0, 16)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
