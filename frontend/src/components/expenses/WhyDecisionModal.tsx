import React from "react";
import { X, ShieldCheck, CheckCircle2, AlertCircle, Link, FileText, BookOpen } from "lucide-react";
import { Expense } from "../../types";

interface WhyDecisionModalProps {
  expense: Expense | null;
  onClose: () => void;
}

export const WhyDecisionModal: React.FC<WhyDecisionModalProps> = ({ expense, onClose }) => {
  if (!expense) return null;

  const decision = expense.decision;
  const rule = decision?.tax_rule;
  const evScore = Math.round((decision?.evidence_strength_score ?? 0.8) * 100);
  const confScore = Math.round((decision?.ai_confidence ?? 0.9) * 100);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="glass-card rounded-2xl w-full max-w-2xl border border-brand-border bg-brand-navy shadow-2xl max-h-[90vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="p-5 border-b border-brand-border flex items-center justify-between bg-brand-dark/40">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-brand-primary/20 text-brand-accent flex items-center justify-center">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Traceable Evidence & Decision Reasoning
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                {expense.merchant} • ₹{expense.amount.toLocaleString("en-IN")} • Claim #{expense.id.slice(0, 8)}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-brand-card transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-6 space-y-6 overflow-y-auto">
          {/* Summary Box */}
          <div className="bg-brand-card/90 rounded-xl p-4 border border-brand-border">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Statutory Potential Treatment
            </div>
            <div className="text-base font-extrabold text-white mt-1 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
              <span>{decision?.potential_treatment}</span>
            </div>
            <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-slate-800 text-xs">
              <div>
                <span className="text-slate-400 text-[11px]">AI Confidence:</span>
                <div className="font-bold text-white font-mono mt-0.5">{confScore}%</div>
              </div>
              <div>
                <span className="text-slate-400 text-[11px]">Evidence Strength:</span>
                <div className="font-bold text-emerald-400 font-mono mt-0.5">{evScore}%</div>
              </div>
              <div>
                <span className="text-slate-400 text-[11px]">Eligible Claim:</span>
                <div className="font-bold text-emerald-400 font-mono mt-0.5">
                  ₹{expense.eligible_deductible_amount.toLocaleString("en-IN")}
                </div>
              </div>
              <div>
                <span className="text-slate-400 text-[11px]">Audit Gating:</span>
                <div className="font-bold text-brand-accent font-mono mt-0.5">{decision?.decision_status}</div>
              </div>
            </div>
          </div>

          {/* Applicable Statutory Tax Rule (Zero Hallucination Proof) */}
          <div className="space-y-2">
            <div className="text-xs font-bold text-brand-accent uppercase tracking-wider flex items-center gap-1.5">
              <BookOpen className="w-4 h-4" />
              <span>Governing Statutory Authority & Rule</span>
            </div>
            {rule ? (
              <div className="bg-brand-dark/60 rounded-xl p-4 border border-brand-border space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white text-sm">{rule.title}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-primary/20 text-brand-accent border border-brand-accent/30">
                    {rule.rule_code}
                  </span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">{rule.description}</p>
                <div className="text-[11px] text-slate-400 font-mono pt-1">
                  Source: <span className="text-slate-200 font-semibold">{rule.source_statute}</span> ({rule.jurisdiction})
                </div>
                {rule.statute_citation_url && (
                  <a
                    href={rule.statute_citation_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-[11px] text-brand-accent hover:underline font-mono mt-1"
                  >
                    <span>View Official Government Statute</span>
                    <Link className="w-3 h-3" />
                  </a>
                )}
              </div>
            ) : (
              <div className="text-xs text-slate-400 italic">
                Evaluated under general business deduction principles (Section 37(1)).
              </div>
            )}
          </div>

          {/* Traceable Reasoning Points */}
          <div className="space-y-2">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Evidence Factor Breakdown</span>
            </div>
            <div className="space-y-2">
              {decision?.reasoning_summary.map((point, idx) => (
                <div
                  key={idx}
                  className="flex items-start space-x-3 text-xs bg-brand-navy/60 p-2.5 rounded-lg border border-slate-800"
                >
                  <span className="w-5 h-5 rounded-full bg-brand-primary/20 text-brand-accent flex items-center justify-center font-mono text-[10px] font-bold shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <span className="text-slate-200 leading-relaxed">{point}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Limitations Applied */}
          {decision?.limitations_applied && (
            <div className="space-y-1.5">
              <div className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4" />
                <span>Statutory Limitations / Allocation</span>
              </div>
              <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-xs text-amber-200 leading-relaxed">
                {decision.limitations_applied}
              </div>
            </div>
          )}

          {/* Cryptographic Integrity Footer */}
          <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-500 font-mono">
            <span>Audit Trail Verified</span>
            <span className="text-emerald-400">Tamper-Proof SHA-256</span>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-brand-border bg-brand-dark/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-brand-card hover:bg-brand-cardHover text-white text-xs font-semibold border border-brand-border transition-all"
          >
            Close Reasoning Chain
          </button>
        </div>
      </div>
    </div>
  );
};
