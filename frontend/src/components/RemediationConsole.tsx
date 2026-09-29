import React, { useState, useEffect } from 'react';
import { Wrench, Terminal, Copy, Check, Play, ShieldAlert, Ticket } from 'lucide-react';
import { getDriftFindings, updateFindingStatus, remediateFinding } from '../services/api';

export const RemediationConsole: React.FC = () => {
  const [findings, setFindings] = useState<any[]>([]);
  const [selectedFinding, setSelectedFinding] = useState<any>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [remediating, setRemediating] = useState<boolean>(false);
  const [actionMsg, setActionMsg] = useState<string>('');

  useEffect(() => {
    loadFindings();
  }, []);

  const loadFindings = async () => {
    try {
      setLoading(true);
      const data = await getDriftFindings();
      setFindings(data);
      if (data.length > 0) {
        setSelectedFinding(data[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    if (!selectedFinding) return;
    try {
      const updated = await updateFindingStatus(selectedFinding.finding_id, newStatus);
      setSelectedFinding(updated);
      setFindings(findings.map(f => f.finding_id === updated.finding_id ? updated : f));
      setActionMsg(`Finding status updated to ${newStatus}`);
      setTimeout(() => setActionMsg(''), 3000);
    } catch (e: any) {
      alert('Error updating status: ' + e.message);
    }
  };

  const handleExecuteRemediation = async () => {
    if (!selectedFinding) return;
    try {
      setRemediating(true);
      const res = await remediateFinding(selectedFinding.finding_id);
      setActionMsg(res.message);
      setSelectedFinding({ ...selectedFinding, status: 'REMEDIATED' });
      setFindings(findings.map(f => f.finding_id === selectedFinding.finding_id ? { ...f, status: 'REMEDIATED' } : f));
      setTimeout(() => setActionMsg(''), 4000);
    } catch (e: any) {
      alert('Remediation error: ' + e.message);
    } font-mono finally {
      setRemediating(false);
    }
  };

  const generateCLIScript = (f: any) => {
    if (!f) return '# Select a finding to view CLI script';
    return `! =========================================================
! CLI REMEDIATION SCRIPT - HOSPITAL DRIFT SENTINEL
! Hostname: ${f.hostname} (Site: ${f.site_id})
! Target Field: ${f.field_name}
! Risk Score: ${f.risk_score} | Authorization: ${f.authorization_status}
! =========================================================
configure terminal
! Target device configuration fix
${f.field_name.toLowerCase().includes('telnet') ? 'no service telnet\nline vty 0 15\n transport input ssh' : 
  f.field_name.toLowerCase().includes('ssh') ? 'ip ssh version 2\nip ssh rsa keypair-name SSH-KEY' :
  f.field_name.toLowerCase().includes('logging') ? 'logging host 10.100.1.50\nlogging trap informational' :
  `no ${f.field_name}\n! Apply approved baseline value\n${f.baseline_value || 'default configuration'}`}
exit
write memory
! End of remediation script`;
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return <div className="p-8 text-slate-400 font-mono text-center">Loading Remediation Console...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-cyan-500/20 text-cyan-400 rounded-2xl border border-cyan-500/30">
            <Wrench className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              Remediation & Evidence Console
              <span className="px-2.5 py-0.5 text-[10px] font-mono font-semibold bg-cyan-500/20 text-cyan-400 rounded-full border border-cyan-500/30">
                Phase 2 Extended
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Interactive CLI Script Generator, CAB Ticket Inspector & Audit Evidence Manager
            </p>
          </div>
        </div>
      </div>

      {actionMsg && (
        <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs font-mono text-emerald-300">
          {actionMsg}
        </div>
      )}

      {/* Main Console Split View */}
      <div className="grid grid-cols-3 gap-6">
        {/* Left Side: Findings List */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col h-[650px]">
          <h3 className="font-bold text-xs text-slate-300 mb-3 uppercase tracking-wider">
            Active Drift Findings ({findings.length})
          </h3>
          <div className="overflow-y-auto space-y-2 flex-1 pr-1 text-xs">
            {findings.map((f: any) => (
              <div
                key={f.finding_id}
                onClick={() => setSelectedFinding(f)}
                className={`p-3 rounded-xl border cursor-pointer transition ${
                  selectedFinding?.finding_id === f.finding_id
                    ? 'bg-cyan-500/10 border-cyan-500/40 text-slate-100'
                    : 'bg-slate-950 border-slate-800/80 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-mono font-bold text-cyan-400">{f.finding_id}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    f.status === 'REMEDIATED' ? 'bg-emerald-500/20 text-emerald-400' :
                    f.status === 'ACKNOWLEDGED' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {f.status}
                  </span>
                </div>
                <p className="font-bold text-slate-200">{f.hostname}</p>
                <p className="font-mono text-[11px] text-slate-400">{f.field_name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: Remediation & CLI Script Terminal */}
        {selectedFinding && (
          <div className="col-span-2 space-y-4">
            {/* Finding Detail Header */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                    {selectedFinding.hostname}
                    <span className="text-xs font-mono text-cyan-400">({selectedFinding.site_id})</span>
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Field: <span className="font-mono text-amber-400">{selectedFinding.field_name}</span> | Type: {selectedFinding.device_type}
                  </p>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleStatusChange('ACKNOWLEDGED')}
                    className="px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded-xl text-xs font-semibold transition"
                  >
                    Acknowledge
                  </button>
                  <button
                    onClick={handleExecuteRemediation}
                    disabled={remediating || selectedFinding.status === 'REMEDIATED'}
                    className="px-4 py-1.5 bg-cyan-500 hover:bg-cyan-400 disabled:bg-slate-800 text-slate-950 font-bold rounded-xl text-xs flex items-center space-x-1.5 transition"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>{remediating ? 'Executing...' : selectedFinding.status === 'REMEDIATED' ? 'Remediated' : 'Execute Fix'}</span>
                  </button>
                </div>
              </div>

              {/* Status & Ticket Banner */}
              <div className="grid grid-cols-3 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
                <div>
                  <span className="text-slate-500">Authorization:</span>
                  <p className="font-bold text-slate-200">{selectedFinding.authorization_status}</p>
                </div>
                <div>
                  <span className="text-slate-500">CAB Ticket ID:</span>
                  <p className="font-mono font-bold text-cyan-400 flex items-center gap-1">
                    <Ticket className="w-3.5 h-3.5" />
                    {selectedFinding.ticket_id || 'NONE (Unauthorized)'}
                  </p>
                </div>
                <div>
                  <span className="text-slate-500">Composite Risk Score:</span>
                  <p className="font-mono font-bold text-red-400">{selectedFinding.risk_score} / 100</p>
                </div>
              </div>
            </div>

            {/* CLI Script Output Terminal */}
            <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
              <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex justify-between items-center text-xs">
                <span className="font-mono text-cyan-400 flex items-center gap-2">
                  <Terminal className="w-4 h-4" />
                  Generated CLI Remediation Commands
                </span>
                <button
                  onClick={() => copyToClipboard(generateCLIScript(selectedFinding))}
                  className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs flex items-center space-x-1 transition"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy Script'}</span>
                </button>
              </div>
              <pre className="p-4 font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed h-72">
                {generateCLIScript(selectedFinding)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
