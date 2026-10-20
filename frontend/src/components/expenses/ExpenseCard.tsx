import React from "react";
import {
  HelpCircle,
  FileQuestion,
  CheckCircle,
  AlertTriangle,
  Receipt,
  Sparkles,
  ShieldCheck,
  Building,
  Clock
} from "lucide-react";
import { Expense } from "../../types";

interface ExpenseCardProps {
  expense: Expense;
  onWhyClick: (expense: Expense) => void;
  onMissingEvidenceClick: (expense: Expense) => void;
  onConfirmClick: (expenseId: string) => void;
}

export const ExpenseCard: React.FC<ExpenseCardProps> = ({
  expense,
  onWhyClick,
  onMissingEvidenceClick,
  onConfirmClick,
}) => {
  const decision = expense.decision;
  const evScore = decision?.evidence_strength_score ?? 0.75;
  const confScore = decision?.ai_confidence ?? 0.90;
  const isConfirmed = expense.status === "CONFIRMED";
  const hasAnomalies = (expense.anomalies?.length ?? 0) > 0;
  const hasMissing = (decision?.missing_evidence?.length ?? 0) > 0;

  // Status Chip Style
  const getStatusBadge = () => {
    if (isConfirmed) {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
          <CheckCircle className="w-3 h-3" /> CONFIRMED
        </span>
      );
    }
    switch (expense.status) {
      case "AUTO_RECOMMENDED":
        return (
          <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-brand-primary/20 text-brand-accent border border-brand-accent/30 flex items-center gap-1 shadow-glow">
            <Sparkles className="w-3 h-3 text-brand-accent" /> AUTO RECOMMENDED
          </span>
        );
      case "NEEDS_REVIEW":
        return (
          <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3 text-amber-400" /> NEEDS REVIEW
          </span>
        );
      case "INSUFFICIENT_DATA":
        return (
          <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-1">
            <FileQuestion className="w-3 h-3 text-rose-400" /> INSUFFICIENT DATA
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className={`glass-card rounded-2xl p-5 border transition-all glass-card-hover ${
      hasAnomalies ? "border-rose-500/40 bg-rose-500/[0.03]" : "border-brand-border"
    }`}>
      {/* Header Row: Merchant, Category, Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-brand-navy border border-brand-border flex items-center justify-center text-slate-300 shadow-inner">
            <Receipt className="w-5 h-5 text-brand-accent" />
          </div>
          <div>
            <h4 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
              <span>{expense.merchant}</span>
              {expense.invoice_number && (
                <span className="text-[10px] text-slate-400 font-mono font-normal">
                  #{expense.invoice_number}
                </span>
              )}
            </h4>
            <div className="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
              <span className="capitalize px-2 py-0.5 rounded-md bg-brand-navy text-[11px] font-medium border border-brand-border text-slate-300">
                {expense.category}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1 font-mono text-[11px]">
                <Clock className="w-3 h-3 text-slate-500" />
                {expense.transaction_date}
              </span>
            </div>
          </div>
        </div>

        {/* Right Status */}
        <div className="flex items-center space-x-2 self-start sm:self-auto">
          {getStatusBadge()}
        </div>
      </div>

      {/* Middle Row: Potential Treatment & Amounts */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        {/* Treatment info */}
        <div className="md:col-span-7">
          <div className="text-[11px] text-slate-400 font-medium">Potential Tax Treatment:</div>
          <div className="text-sm font-semibold text-slate-100 flex items-center gap-1.5 mt-0.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span className="truncate">{decision?.potential_treatment || "Pending statutory evaluation"}</span>
          </div>
          {expense.business_purpose && (
            <p className="text-[11px] text-slate-400 italic mt-1 line-clamp-1">
              "{expense.business_purpose}"
            </p>
          )}
        </div>

        {/* Amount & Claimable */}
        <div className="md:col-span-5 flex items-center justify-start md:justify-end space-x-6">
          <div>
            <div className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Gross Amount</div>
            <div className="text-base font-bold text-slate-300 font-mono">
              ₹{expense.amount.toLocaleString("en-IN")}
            </div>
          </div>
          <div className="text-right">
            <div className="text-[10px] uppercase tracking-wider text-emerald-400 font-bold">Deductible</div>
            <div className="text-lg font-black text-emerald-400 font-mono">
              ₹{expense.eligible_deductible_amount.toLocaleString("en-IN")}
            </div>
          </div>
        </div>
      </div>

      {/* Anomaly / Alert Banner if present */}
      {hasAnomalies && (
        <div className="mt-3.5 bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 flex items-start space-x-2.5">
          <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div className="text-xs text-rose-200">
            <span className="font-bold">Risk Flag ({expense.anomalies![0].anomaly_type}): </span>
            <span>{expense.anomalies![0].explanation}</span>
          </div>
        </div>
      )}

      {/* Footer Controls: Scores & Action Buttons */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        {/* Scores */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1.5">
            <span className="text-[11px] text-slate-400">AI Confidence:</span>
            <span className="text-xs font-bold text-white font-mono bg-brand-navy px-2 py-0.5 rounded border border-brand-border">
              {Math.round(confScore * 100)}%
            </span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="text-[11px] text-slate-400">Evidence Strength:</span>
            <span className={`text-xs font-bold font-mono px-2 py-0.5 rounded border ${
              evScore >= 0.80
                ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                : "bg-amber-500/10 text-amber-400 border-amber-500/30"
            }`}>
              {Math.round(evScore * 100)}%
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-2 self-end sm:self-auto">
          {/* Why Button */}
          <button
            onClick={() => onWhyClick(expense)}
            className="px-3 py-1.5 rounded-xl bg-brand-navy hover:bg-brand-cardHover border border-brand-border text-slate-200 hover:text-white text-xs font-semibold flex items-center space-x-1.5 transition-all shadow-sm"
          >
            <HelpCircle className="w-3.5 h-3.5 text-brand-primary" />
            <span>Why TaxClaim Decided This?</span>
          </button>

          {/* Missing Evidence Button */}
          {hasMissing && (
            <button
              onClick={() => onMissingEvidenceClick(expense)}
              className="px-3 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 text-xs font-semibold flex items-center space-x-1.5 transition-all"
            >
              <FileQuestion className="w-3.5 h-3.5" />
              <span>Missing Evidence</span>
            </button>
          )}

          {/* Confirm Button */}
          {!isConfirmed && (
            <button
              onClick={() => onConfirmClick(expense.id)}
              className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center space-x-1.5 transition-all shadow-glowCyan"
            >
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Confirm Claim</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
