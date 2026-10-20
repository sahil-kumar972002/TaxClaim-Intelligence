import React, { useState } from "react";
import { X, FileQuestion, ArrowRight, CheckCircle2, ShieldAlert } from "lucide-react";
import { Expense } from "../../types";

interface MissingEvidenceModalProps {
  expense: Expense | null;
  onClose: () => void;
  onSubmitPatch: (
    expenseId: string,
    patch: {
      business_purpose?: string;
      business_use_percentage?: number;
      payment_proof_reference?: string;
    }
  ) => Promise<void>;
}

export const MissingEvidenceModal: React.FC<MissingEvidenceModalProps> = ({
  expense,
  onClose,
  onSubmitPatch,
}) => {
  if (!expense) return null;

  const [purpose, setPurpose] = useState(expense.business_purpose || "");
  const [usePct, setUsePct] = useState(Math.round(expense.business_use_percentage * 100));
  const [paymentRef, setPaymentRef] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const missingItems = expense.decision?.missing_evidence || [];

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmitPatch(expense.id, {
        business_purpose: purpose,
        business_use_percentage: usePct / 100.0,
        payment_proof_reference: paymentRef || undefined,
      });
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="glass-card rounded-2xl w-full max-w-lg border border-brand-border bg-brand-navy shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-brand-border flex items-center justify-between bg-brand-dark/40">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center">
              <FileQuestion className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Missing Evidence Copilot
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                {expense.merchant} • Current Score: {Math.round((expense.decision?.evidence_strength_score ?? 0.7) * 100)}%
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSave} className="p-6 space-y-5">
          <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3.5 text-xs text-amber-200 leading-relaxed">
            <p className="font-bold mb-1 flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              TaxClaim Needs Additional Substantiation
            </p>
            Your {expense.merchant} expense appears potentially business-related, but requires specific evidence points to satisfy audit criteria and maximize deductibility.
          </div>

          {/* Missing Questions Checklist */}
          {missingItems.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                Missing Statutory Elements:
              </span>
              <ul className="space-y-1">
                {missingItems.map((m, idx) => (
                  <li key={idx} className="text-xs text-rose-300 flex items-start gap-1.5">
                    <span className="text-rose-400 font-bold">•</span>
                    <span>{m.prompt}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Question 1: Business Purpose Nexus */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300 flex items-center justify-between">
              <span>Business Purpose & Client Nexus</span>
              <span className="text-[10px] text-slate-500 font-normal">Section 37(1) requirement</span>
            </label>
            <textarea
              rows={2}
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              placeholder="e.g. Workstation used for client microservices development and code compilation."
              className="w-full glass-input rounded-xl p-3 text-xs focus:ring-1 focus:ring-brand-primary"
            />
          </div>

          {/* Question 2: Business-Use Percentage */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-xs font-bold text-slate-300">
              <span>Business-Use Allocation:</span>
              <span className="text-brand-accent font-mono">{usePct}% Business</span>
            </div>
            <input
              type="range"
              min="10"
              max="100"
              step="5"
              value={usePct}
              onChange={(e) => setUsePct(Number(e.target.value))}
              className="w-full accent-brand-primary cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>10% (Occasional)</span>
              <span>50% (Shared)</span>
              <span>100% (Pure Business)</span>
            </div>
          </div>

          {/* Question 3: Bank / Card Reference */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300 flex items-center justify-between">
              <span>Proof of Payment / Bank Ref (Optional)</span>
              <span className="text-[10px] text-slate-500 font-normal">Non-cash audit trail</span>
            </label>
            <input
              type="text"
              value={paymentRef}
              onChange={(e) => setPaymentRef(e.target.value)}
              placeholder="e.g. HDFC Credit Card Ref 4092 or UPI 429108"
              className="w-full glass-input rounded-xl px-3 py-2 text-xs"
            />
          </div>

          {/* Score Boost Preview */}
          <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
            <div className="text-xs text-slate-400">
              Estimated Score Boost: <span className="font-bold text-emerald-400 font-mono">+18%</span>
            </div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs font-bold shadow-glow flex items-center space-x-1.5 transition-all disabled:opacity-50"
            >
              <span>{isSubmitting ? "Submitting..." : "Update Evidence"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
