import React, { useState, useEffect } from "react";
import {
  Activity,
  ShieldAlert,
  Database,
  Cpu,
  RefreshCw,
  BookOpen,
  CheckCircle2,
  AlertTriangle,
  History,
  TrendingDown
} from "lucide-react";
import { api } from "../../services/api";
import { TaxRule } from "../../types";

export const AdminView: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [rules, setRules] = useState<TaxRule[]>([]);
  const [activeTab, setActiveTab] = useState<"metrics" | "rules" | "audit">("metrics");
  const [isResetting, setIsResetting] = useState(false);

  const fetchData = async () => {
    try {
      const [m, logs, r] = await Promise.all([
        api.getModelMetrics(),
        api.getAuditLogs(),
        api.getTaxRules(),
      ]);
      setMetrics(m);
      setAuditLogs(logs);
      setRules(r);
    } catch (err) {
      console.error("Admin fetch error", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSeedReset = async () => {
    setIsResetting(true);
    try {
      await api.seedDemo();
      await fetchData();
      alert("Demo data successfully re-seeded!");
    } catch (err) {
      console.error(err);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-brand-primary" />
            <span>AI Model Governance & Regulatory Administration</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Monitor ML inference accuracy, concept drift, statutory rule versioning, and immutable audit logs.
          </p>
        </div>

        <button
          onClick={handleSeedReset}
          disabled={isResetting}
          className="px-4 py-2 rounded-xl bg-brand-navy hover:bg-brand-cardHover border border-brand-border text-slate-200 text-xs font-semibold flex items-center space-x-2 transition-all shadow-sm"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isResetting ? "animate-spin" : ""}`} />
          <span>Reset Demo Data</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-brand-border pb-2 text-xs">
        <button
          onClick={() => setActiveTab("metrics")}
          className={`px-3 py-1.5 rounded-lg font-bold transition-all ${
            activeTab === "metrics"
              ? "bg-brand-primary text-white"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Model Performance & Drift
        </button>
        <button
          onClick={() => setActiveTab("rules")}
          className={`px-3 py-1.5 rounded-lg font-bold transition-all ${
            activeTab === "rules"
              ? "bg-brand-primary text-white"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Statutory Rule Manager ({rules.length})
        </button>
        <button
          onClick={() => setActiveTab("audit")}
          className={`px-3 py-1.5 rounded-lg font-bold transition-all ${
            activeTab === "audit"
              ? "bg-brand-primary text-white"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Security Audit Logs ({auditLogs.length})
        </button>
      </div>

      {/* Tab 1: Model Metrics & Drift */}
      {activeTab === "metrics" && metrics && (
        <div className="space-y-6">
          {/* Top Metric Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="glass-card rounded-2xl p-4 border border-brand-border">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Accuracy</span>
              <div className="text-2xl font-black text-emerald-400 font-mono mt-1">
                {(metrics.overall_accuracy * 100).toFixed(1)}%
              </div>
              <div className="text-[10px] text-slate-500">Validation & Confirmation Match</div>
            </div>

            <div className="glass-card rounded-2xl p-4 border border-brand-border">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">F1-Score</span>
              <div className="text-2xl font-black text-brand-accent font-mono mt-1">
                {(metrics.f1_score * 100).toFixed(1)}%
              </div>
              <div className="text-[10px] text-slate-500">Macro Balanced F1</div>
            </div>

            <div className="glass-card rounded-2xl p-4 border border-brand-border">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Concept Drift (PSI)</span>
              <div className="text-2xl font-black text-emerald-400 font-mono mt-1">
                {metrics.drift_index_psi}
              </div>
              <div className="text-[10px] text-emerald-400 font-semibold">{metrics.drift_status} (&lt;0.10)</div>
            </div>

            <div className="glass-card rounded-2xl p-4 border border-brand-border">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Avg Latency</span>
              <div className="text-2xl font-black text-white font-mono mt-1">
                {metrics.avg_inference_latency_ms}ms
              </div>
              <div className="text-[10px] text-slate-500">Fast In-Memory Classifier</div>
            </div>
          </div>

          {/* Confusion Matrix & Confidence Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Confusion Matrix Table */}
            <div className="lg:col-span-7 glass-card rounded-2xl p-5 border border-brand-border space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white">Confusion Matrix (Multi-Class Evaluation)</h3>
                  <p className="text-[11px] text-slate-400">Predicted Category vs User Ground Truth Confirmation</p>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-navy border border-brand-border text-slate-300">
                  Total: {metrics.total_inferences} Inferences
                </span>
              </div>

              {metrics.confusion_matrix && (
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 font-mono text-[10px] uppercase">
                        <th className="py-2 px-3">Actual \ Predicted</th>
                        {metrics.confusion_matrix.labels.map((lbl: string) => (
                          <th key={lbl} className="py-2 px-3 text-center">{lbl}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                      {metrics.confusion_matrix.labels.map((rowLabel: string, rIdx: number) => (
                        <tr key={rowLabel} className="hover:bg-brand-navy/40">
                          <td className="py-2.5 px-3 font-bold text-slate-300 capitalize">{rowLabel}</td>
                          {metrics.confusion_matrix.matrix[rIdx].map((val: number, cIdx: number) => {
                            const isDiagonal = rIdx === cIdx;
                            return (
                              <td
                                key={cIdx}
                                className={`py-2.5 px-3 text-center font-bold ${
                                  isDiagonal
                                    ? "bg-brand-primary/10 text-brand-accent"
                                    : val > 0
                                    ? "text-rose-400 bg-rose-500/5"
                                    : "text-slate-600"
                                }`}
                              >
                                {val}
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Confidence Histogram */}
            <div className="lg:col-span-5 glass-card rounded-2xl p-5 border border-brand-border space-y-4 flex flex-col justify-between">
              <div>
                <h3 className="text-sm font-bold text-white">Confidence Score Distribution</h3>
                <p className="text-[11px] text-slate-400">Probability calibration across evaluated claims</p>
              </div>

              <div className="space-y-3">
                {metrics.confidence_distribution?.map((item: any, idx: number) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-300 font-bold">{item.bin}</span>
                      <span className="text-brand-accent font-semibold">{item.count} items ({item.pct}%)</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-brand-primary to-brand-accent"
                        style={{ width: `${item.pct}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="text-[10px] text-slate-500 font-mono pt-2 border-t border-slate-800 flex justify-between">
                <span>Human Override Rate:</span>
                <span className="text-slate-300 font-bold">{(metrics.human_overrides_rate * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Statutory Rule Manager */}
      {activeTab === "rules" && (
        <div className="glass-card rounded-2xl border border-brand-border overflow-hidden">
          <div className="p-4 border-b border-brand-border bg-brand-dark/40 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white">Verified Statutory Rules Repository</h3>
              <p className="text-[11px] text-slate-400">Zero-hallucination ground truth statutory knowledge base</p>
            </div>
          </div>

          <div className="divide-y divide-slate-800 overflow-x-auto">
            {rules.map((rule) => (
              <div key={rule.rule_code} className="p-4 hover:bg-brand-navy/30 transition-colors space-y-2">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-brand-accent bg-brand-primary/10 border border-brand-accent/30 px-2 py-0.5 rounded">
                      {rule.rule_code}
                    </span>
                    <span className="text-sm font-bold text-white">{rule.title}</span>
                  </div>
                  <span className="text-xs font-mono text-emerald-400 font-bold self-start sm:self-auto">
                    {rule.deductibility_status}
                  </span>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">{rule.description}</p>

                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-slate-400 font-mono pt-1">
                  <span>Country: <b className="text-slate-200">{rule.country}</b></span>
                  <span>Jurisdiction: <b className="text-slate-200">{rule.jurisdiction}</b></span>
                  <span>Source: <b className="text-slate-200">{rule.source_statute}</b></span>
                  <span>Version: <b className="text-brand-accent">{rule.rule_version}</b></span>
                  <span>Last Verified: <b className="text-slate-200">{rule.last_verified_date}</b></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Security Audit Logs */}
      {activeTab === "audit" && (
        <div className="glass-card rounded-2xl border border-brand-border overflow-hidden">
          <div className="p-4 border-b border-brand-border bg-brand-dark/40 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white">Immutable Security Audit Trail</h3>
              <p className="text-[11px] text-slate-400">Comprehensive cryptographic event ledger for compliance</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-mono text-[10px] uppercase bg-brand-navy/60">
                  <th className="py-2.5 px-4">Timestamp</th>
                  <th className="py-2.5 px-4">Action</th>
                  <th className="py-2.5 px-4">Resource</th>
                  <th className="py-2.5 px-4">IP Address</th>
                  <th className="py-2.5 px-4">Payload Summary</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-brand-navy/30">
                    <td className="py-2.5 px-4 text-slate-400">{log.timestamp?.slice(0, 19).replace("T", " ")}</td>
                    <td className="py-2.5 px-4 font-bold text-brand-accent">{log.action}</td>
                    <td className="py-2.5 px-4 text-slate-300">{log.resource_type}:{log.resource_id?.slice(0, 8)}</td>
                    <td className="py-2.5 px-4 text-slate-500">{log.ip_address}</td>
                    <td className="py-2.5 px-4 text-slate-400 truncate max-w-xs">
                      {JSON.stringify(log.diff_payload || {})}
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
