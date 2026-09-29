import React from 'react';
import { X, CheckCircle, AlertTriangle, FileCode } from 'lucide-react';

interface DiffViewerModalProps {
  finding: any;
  onClose: () => void;
  onRemediate?: (id: string) => void;
}

export const DiffViewerModal: React.FC<DiffViewerModalProps> = ({ finding, onClose, onRemediate }) => {
  if (!finding) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-cyan-500/20 text-cyan-400 rounded-xl">
              <FileCode className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-sm text-slate-100">Configuration Drift Inspector</h3>
              <p className="text-xs text-slate-400">Hostname: <span className="font-mono text-cyan-400">{finding.hostname}</span> | Field: <span className="font-mono text-amber-400">{finding.field_name}</span></p>
            </div>
          </div>
          <button 
            onClick={onClose} 
            className="text-slate-400 hover:text-slate-100 p-1.5 hover:bg-slate-800 rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-xs">
          {/* Risk Summary Badge Bar */}
          <div className="grid grid-cols-4 gap-4 p-4 bg-slate-950 rounded-xl border border-slate-800">
            <div>
              <p className="text-slate-400 text-[11px]">Severity</p>
              <p className={`font-bold ${finding.severity === 'CRITICAL' ? 'text-red-400' : finding.severity === 'HIGH' ? 'text-orange-400' : 'text-amber-400'}`}>{finding.severity}</p>
            </div>
            <div>
              <p className="text-slate-400 text-[11px]">Composite Risk Score</p>
              <p className="font-mono font-bold text-cyan-400">{finding.risk_score} / 100</p>
            </div>
            <div>
              <p className="text-slate-400 text-[11px]">Authorization</p>
              <p className={`font-bold ${finding.authorization_status === 'Authorized' ? 'text-emerald-400' : 'text-red-400'}`}>{finding.authorization_status}</p>
            </div>
            <div>
              <p className="text-slate-400 text-[11px]">Compliance Status</p>
              <p className={`font-bold ${finding.compliance_status === 'Violation' ? 'text-red-400' : 'text-emerald-400'}`}>{finding.compliance_status}</p>
            </div>
          </div>

          {/* Side-by-Side Diff Comparison */}
          <div>
            <h4 className="font-bold text-xs mb-3 text-slate-300 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Side-by-Side Configuration Diff
            </h4>
            <div className="grid grid-cols-2 gap-4">
              {/* Approved Baseline */}
              <div className="bg-slate-950 p-4 rounded-xl border border-emerald-500/30">
                <div className="flex justify-between items-center mb-2 pb-2 border-b border-slate-800">
                  <span className="font-semibold text-emerald-400 flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5" /> Approved Baseline Value
                  </span>
                  <span className="font-mono text-[10px] text-slate-500">v1.2-Baseline</span>
                </div>
                <pre className="font-mono text-emerald-300/90 whitespace-pre-wrap bg-slate-900/60 p-3 rounded-lg border border-slate-800/80">
                  {finding.baseline_value || 'NULL (Not Present)'}
                </pre>
              </div>

              {/* Running Config */}
              <div className="bg-slate-950 p-4 rounded-xl border border-red-500/30">
                <div className="flex justify-between items-center mb-2 pb-2 border-b border-slate-800">
                  <span className="font-semibold text-red-400 flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5" /> Active Running Config (Drifted)
                  </span>
                  <span className="font-mono text-[10px] text-slate-500">Live Device State</span>
                </div>
                <pre className="font-mono text-red-300/90 whitespace-pre-wrap bg-slate-900/60 p-3 rounded-lg border border-slate-800/80">
                  {finding.current_value || 'NULL (Removed)'}
                </pre>
              </div>
            </div>
          </div>

          {/* Forensic Audit Evidence */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <h4 className="font-bold text-xs mb-2 text-slate-300">Forensic Audit Evidence</h4>
            <p className="font-mono text-slate-300 bg-slate-900 p-3 rounded-lg border border-slate-800/60 leading-relaxed">
              {finding.evidence}
            </p>
          </div>

          {/* Recommended Action */}
          <div className="bg-slate-950 p-4 rounded-xl border border-cyan-500/20">
            <h4 className="font-bold text-xs mb-2 text-cyan-400">Recommended Resolution</h4>
            <p className="text-slate-300">{finding.recommended_action}</p>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-slate-800 flex justify-between items-center bg-slate-900/50">
          <span className="text-[11px] text-slate-500 font-mono">Finding ID: {finding.finding_id}</span>
          <div className="flex items-center space-x-3">
            <button 
              onClick={onClose} 
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-xl text-xs transition"
            >
              Close
            </button>
            {onRemediate && (
              <button 
                onClick={() => { onRemediate(finding.finding_id); onClose(); }}
                className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl text-xs transition flex items-center space-x-1.5"
              >
                <span>Execute Remediation</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
