import React from "react";
import {
  ShieldCheck,
  Award,
  DollarSign,
  AlertCircle,
  AlertTriangle
} from "lucide-react";

interface MetricCardsProps {
  healthScore: number;
  avgEvidenceScore: number;
  potentialClaims: number;
  needsReviewCount: number;
  riskAlertCount: number;
  onFilterReview?: () => void;
  onFilterRisk?: () => void;
}

export const MetricCards: React.FC<MetricCardsProps> = ({
  healthScore,
  avgEvidenceScore,
  potentialClaims,
  needsReviewCount,
  riskAlertCount,
  onFilterReview,
  onFilterRisk,
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      {/* 1. Tax Health */}
      <div className="glass-card rounded-2xl p-4 border border-brand-border glass-card-hover">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Tax Health</span>
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 text-2xl font-black text-white font-mono">{healthScore}/100</div>
        <div className="mt-1 text-[11px] text-emerald-400 font-medium">Audit Defense Tier A</div>
      </div>

      {/* 2. Evidence Strength */}
      <div className="glass-card rounded-2xl p-4 border border-brand-border glass-card-hover">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Evidence Strength</span>
          <div className="w-8 h-8 rounded-lg bg-brand-primary/10 text-brand-primary flex items-center justify-center">
            <Award className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 text-2xl font-black text-brand-accent font-mono">
          {Math.round(avgEvidenceScore * 100)}%
        </div>
        <div className="mt-1 text-[11px] text-slate-400 font-medium">7-Factor Weighted Index</div>
      </div>

      {/* 3. Potential Claims */}
      <div className="glass-card rounded-2xl p-4 border border-brand-border glass-card-hover">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Potential Claims</span>
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <DollarSign className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 text-2xl font-black text-emerald-400 font-mono">
          ₹{potentialClaims.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
        </div>
        <div className="mt-1 text-[11px] text-slate-400 font-medium">Eligible deductions</div>
      </div>

      {/* 4. Needs Review */}
      <div
        onClick={onFilterReview}
        className="glass-card rounded-2xl p-4 border border-amber-500/30 glass-card-hover cursor-pointer bg-amber-500/5"
      >
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-amber-300">Needs Review</span>
          <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center">
            <AlertCircle className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 text-2xl font-black text-amber-400 font-mono">{needsReviewCount}</div>
        <div className="mt-1 text-[11px] text-amber-300/80 font-medium">Missing business justification</div>
      </div>

      {/* 5. Risk Alerts */}
      <div
        onClick={onFilterRisk}
        className="glass-card rounded-2xl p-4 border border-rose-500/30 glass-card-hover cursor-pointer bg-rose-500/5"
      >
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold uppercase tracking-wider text-rose-300">Risk Alerts</span>
          <div className="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center">
            <AlertTriangle className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-2 text-2xl font-black text-rose-400 font-mono">{riskAlertCount}</div>
        <div className="mt-1 text-[11px] text-rose-300/80 font-medium">Duplicate / Spike flagged</div>
      </div>
    </div>
  );
};
