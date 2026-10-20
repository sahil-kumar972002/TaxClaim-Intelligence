import React from "react";
import {
  Cpu,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  Receipt,
  FileCheck,
  TrendingUp,
  Activity
} from "lucide-react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer
} from "recharts";
import { DigitalTwinSummary } from "../../types";

interface DigitalTwinViewProps {
  data: DigitalTwinSummary | null;
}

export const DigitalTwinView: React.FC<DigitalTwinViewProps> = ({ data }) => {
  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Cpu className="w-5 h-5 text-brand-accent" />
          <span>Tax Digital Twin & Ongoing Financial Representation</span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Continuously synchronized representation of your tax profile, documentation health, and audit defense posture.
        </p>
      </div>

      {/* 4 Financial Profile Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-card rounded-2xl p-4 border border-brand-border">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Tax Year & Regime</span>
          <div className="text-base font-bold text-white mt-1">AY {data.tax_year}</div>
          <div className="text-xs text-brand-accent font-medium mt-0.5">{data.current_regime}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-brand-border">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Total Inflow Tracked</span>
          <div className="text-xl font-black text-white font-mono mt-1">
            ₹{data.total_income_tracked.toLocaleString("en-IN")}
          </div>
          <div className="text-[11px] text-slate-400">Annual Professional Receipts</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-brand-border">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Total Claimable</span>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">
            ₹{data.total_potentially_deductible.toLocaleString("en-IN")}
          </div>
          <div className="text-[11px] text-emerald-400/80">
            ₹{data.estimated_tax_savings.toLocaleString("en-IN")} Est. Tax Savings
          </div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-brand-border">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Audit Defense Readiness</span>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">
            {data.audit_readiness_score}/100
          </div>
          <div className="text-[11px] text-slate-400">Tier A Audit Quality</div>
        </div>
      </div>

      {/* Radar Chart & Proactive Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radar Chart: 6 Audit Dimensions */}
        <div className="lg:col-span-6 glass-card rounded-2xl p-5 border border-brand-border flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white">Tax Documentation & Defense Radar</h3>
            <p className="text-[11px] text-slate-400">Multi-dimensional assessment across statutory requirements</p>
          </div>

          <div className="w-full h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data.radar_metrics}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94A3B8" fontSize={11} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" fontSize={9} />
                <Radar
                  name="Audit Score"
                  dataKey="score"
                  stroke="#6366F1"
                  fill="#6366F1"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[10px] text-slate-500 font-mono text-center pt-1 border-t border-slate-800">
            6 statutory dimensions evaluated concurrently
          </div>
        </div>

        {/* Proactive AI Insights */}
        <div className="lg:col-span-6 space-y-4">
          <div className="glass-card rounded-2xl p-5 border border-brand-border h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-brand-accent mb-3">
                <Lightbulb className="w-4 h-4 text-amber-400" />
                <span>Proactive Tax Health Insights</span>
              </div>

              <div className="space-y-3">
                {data.proactive_insights.map((insight, idx) => (
                  <div
                    key={idx}
                    className={`rounded-xl p-3.5 border text-xs leading-relaxed ${
                      insight.severity === "CRITICAL"
                        ? "bg-rose-500/10 border-rose-500/30 text-rose-200"
                        : insight.severity === "WARNING"
                        ? "bg-amber-500/10 border-amber-500/30 text-amber-200"
                        : "bg-brand-primary/10 border-brand-primary/30 text-slate-200"
                    }`}
                  >
                    <div className="font-bold mb-1 flex items-center gap-1.5">
                      {insight.severity === "CRITICAL" ? (
                        <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
                      ) : (
                        <ShieldCheck className="w-4 h-4 text-brand-accent shrink-0" />
                      )}
                      <span>{insight.title}</span>
                    </div>
                    <p className="text-[11px] opacity-90">{insight.message}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Digital Twin Sync Status:</span>
              <span className="text-emerald-400 font-bold font-mono">Live Sync Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
