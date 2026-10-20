import React from "react";
import { Sparkles, ShieldCheck, ArrowUpRight } from "lucide-react";

interface TaxHealthHeaderProps {
  profession: string;
  taxYear: string;
  regime: string;
  readinessScore: number;
  potentialSavings: number;
}

export const TaxHealthHeader: React.FC<TaxHealthHeaderProps> = ({
  profession,
  taxYear,
  regime,
  readinessScore,
  potentialSavings,
}) => {
  return (
    <div className="glass-card rounded-2xl p-6 border border-brand-border bg-gradient-to-r from-brand-card via-brand-navy/90 to-brand-card relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-brand-primary/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>
      <div className="absolute bottom-0 left-1/3 w-60 h-60 bg-brand-accent/10 rounded-full blur-2xl pointer-events-none"></div>

      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-brand-accent tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Tax Command Center</span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400 font-mono">{profession}</span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400 font-mono">AY {taxYear}</span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold text-white mt-1.5 tracking-tight">
            TaxClaim Intelligence
          </h1>
          <p className="text-slate-400 text-xs md:text-sm mt-1 max-w-2xl leading-relaxed">
            Turn your financial documents into evidence-backed, jurisdiction-aware tax intelligence.
            Strict statutory grounding with zero hallucination.
          </p>
        </div>

        {/* Right Health & Potential Savings Callout */}
        <div className="flex items-center space-x-4">
          <div className="bg-brand-navy/90 border border-brand-border rounded-xl px-5 py-3 shadow-inner text-right">
            <div className="text-[11px] font-medium text-slate-400">Potential Tax Savings</div>
            <div className="text-xl md:text-2xl font-black text-emerald-400 font-mono mt-0.5">
              ₹{potentialSavings.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">Based on active claims</div>
          </div>

          <div className="glass-card rounded-xl p-3 border border-emerald-500/30 flex items-center space-x-3 shadow-glowCyan">
            <div className="relative w-12 h-12 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-slate-800"
                  strokeWidth="3.5"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-emerald-400"
                  strokeDasharray={`${readinessScore}, 100`}
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <span className="absolute text-xs font-bold text-white font-mono">{readinessScore}%</span>
            </div>
            <div>
              <div className="text-xs font-bold text-white">Tax Health</div>
              <div className="text-[10px] text-emerald-400 font-semibold flex items-center gap-0.5">
                <ShieldCheck className="w-3 h-3" /> Audit Ready
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
