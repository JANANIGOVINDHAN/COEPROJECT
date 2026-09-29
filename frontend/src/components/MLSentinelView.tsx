import React, { useState, useEffect } from 'react';
import { Cpu, RefreshCw, CheckCircle2, Zap, BarChart3, ShieldCheck } from 'lucide-react';
import { getMLMetrics, retrainMLModels } from '../services/api';

export const MLSentinelView: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [retraining, setRetraining] = useState<boolean>(false);
  const [msg, setMsg] = useState<string>('');

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const data = await getMLMetrics();
      setMetrics(data);
    } catch (e: any) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async () => {
    try {
      setRetraining(true);
      setMsg('Retraining Random Forest Classifier & Isolation Forest...');
      const res = await retrainMLModels();
      setMetrics(res.metrics);
      setMsg('Models successfully retrained with current snapshot feature vectors!');
      setTimeout(() => setMsg(''), 4000);
    } catch (e: any) {
      setMsg('Error retraining models: ' + e.message);
    } finally {
      setRetraining(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono flex items-center justify-center space-x-3">
        <RefreshCw className="w-5 h-5 animate-spin text-cyan-400" />
        <span>Loading ML Sentinel Metrics...</span>
      </div>
    );
  }

  if (!metrics) return null;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex justify-between items-center bg-slate-900 border border-slate-800 p-6 rounded-2xl">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-cyan-500/20 text-cyan-400 rounded-2xl border border-cyan-500/30">
            <Cpu className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              Machine Learning Anomaly & Risk Sentinel
              <span className="px-2.5 py-0.5 text-[10px] font-mono font-semibold bg-emerald-500/20 text-emerald-400 rounded-full border border-emerald-500/30">
                Phase 2 Active
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Isolation Forest (Unsupervised Anomaly) + Random Forest Classifier (Risk Categorization)
            </p>
          </div>
        </div>

        <button
          onClick={handleRetrain}
          disabled={retraining}
          className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-slate-800 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center space-x-2 transition"
        >
          <RefreshCw className={`w-4 h-4 ${retraining ? 'animate-spin' : ''}`} />
          <span>{retraining ? 'Retraining...' : 'Re-evaluate & Retrain Models'}</span>
        </button>
      </div>

      {msg && (
        <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-xs font-mono text-cyan-300">
          {msg}
        </div>
      )}

      {/* KPI Performance Metrics */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
          <p className="text-xs text-slate-400 flex items-center justify-between">
            <span>Accuracy</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </p>
          <h3 className="text-3xl font-mono font-bold text-emerald-400 mt-2">
            {(metrics.accuracy * 100).toFixed(1)}%
          </h3>
          <p className="text-[11px] text-slate-500 mt-1">Test Samples: {metrics.test_samples}</p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
          <p className="text-xs text-slate-400 flex items-center justify-between">
            <span>Precision</span>
            <Zap className="w-4 h-4 text-cyan-400" />
          </p>
          <h3 className="text-3xl font-mono font-bold text-cyan-400 mt-2">
            {(metrics.precision * 100).toFixed(1)}%
          </h3>
          <p className="text-[11px] text-slate-500 mt-1">Weighted Precision</p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
          <p className="text-xs text-slate-400 flex items-center justify-between">
            <span>Recall</span>
            <ShieldCheck className="w-4 h-4 text-purple-400" />
          </p>
          <h3 className="text-3xl font-mono font-bold text-purple-400 mt-2">
            {(metrics.recall * 100).toFixed(1)}%
          </h3>
          <p className="text-[11px] text-slate-500 mt-1">Weighted Recall</p>
        </div>

        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800">
          <p className="text-xs text-slate-400 flex items-center justify-between">
            <span>F1-Score</span>
            <BarChart3 className="w-4 h-4 text-amber-400" />
          </p>
          <h3 className="text-3xl font-mono font-bold text-amber-400 mt-2">
            {(metrics.f1_score * 100).toFixed(1)}%
          </h3>
          <p className="text-[11px] text-slate-500 mt-1">Harmonic Mean</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Confusion Matrix Table */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5">
          <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-cyan-400" />
            Confusion Matrix (Risk Classification)
          </h3>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <table className="w-full text-center text-xs font-mono">
              <thead>
                <tr className="text-slate-400 border-b border-slate-800">
                  <th className="p-2 text-left">Actual \ Predicted</th>
                  <th className="p-2 text-blue-400">LOW</th>
                  <th className="p-2 text-amber-400">MEDIUM</th>
                  <th className="p-2 text-orange-400">HIGH</th>
                  <th className="p-2 text-red-400">CRITICAL</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {metrics.confusion_matrix && metrics.confusion_matrix.map((row: number[], idx: number) => {
                  const labels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
                  return (
                    <tr key={idx}>
                      <td className="p-2 text-left font-bold text-slate-300">{labels[idx] || `Class ${idx}`}</td>
                      {row.map((val: number, cIdx: number) => (
                        <td key={cIdx} className={`p-2 font-bold ${idx === cIdx ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded' : 'text-slate-500'}`}>
                          {val}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Feature Importance Rankings */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5">
          <h3 className="font-bold text-sm text-slate-200 mb-4 flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            Feature Importance Weightings
          </h3>
          <div className="space-y-3 font-mono text-xs">
            {metrics.feature_importances && Object.entries(metrics.feature_importances).map(([feat, val]: [string, any]) => (
              <div key={feat}>
                <div className="flex justify-between text-[11px] mb-1">
                  <span className="text-slate-300">{feat}</span>
                  <span className="text-cyan-400 font-bold">{(val * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div 
                    className="bg-cyan-500 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${Math.max(5, val * 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
