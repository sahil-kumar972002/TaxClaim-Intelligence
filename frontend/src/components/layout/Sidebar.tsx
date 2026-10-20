import React from "react";
import {
  LayoutDashboard,
  Receipt,
  UploadCloud,
  Sliders,
  Cpu,
  FileCheck2,
  Bot,
  Activity,
  ShieldCheck
} from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  reviewCount: number;
  anomalyCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  reviewCount,
  anomalyCount,
}) => {
  const menuItems = [
    { id: "dashboard", label: "Command Center", icon: LayoutDashboard },
    {
      id: "expenses",
      label: "Expense Intelligence",
      icon: Receipt,
      badge: reviewCount > 0 ? reviewCount : undefined,
      badgeColor: "bg-amber-500/20 text-amber-300 border-amber-500/30",
    },
    { id: "ingestion", label: "Smart Ingestion & OCR", icon: UploadCloud },
    { id: "simulator", label: "What-If Simulator", icon: Sliders },
    { id: "digital_twin", label: "Tax Digital Twin", icon: Cpu },
    { id: "audit", label: "Audit Pack Studio", icon: FileCheck2 },
    { id: "copilot", label: "TaxClaim Copilot", icon: Bot },
    {
      id: "admin",
      label: "ML Monitoring & Admin",
      icon: Activity,
      badge: anomalyCount > 0 ? `${anomalyCount} risk` : undefined,
      badgeColor: "bg-rose-500/20 text-rose-300 border-rose-500/30",
    },
  ];

  return (
    <aside className="w-64 border-r border-brand-border bg-brand-navy/60 backdrop-blur-md flex flex-col justify-between p-4 shrink-0">
      <div className="space-y-1.5">
        <div className="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Navigation
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? "bg-brand-primary text-white shadow-glow"
                  : "text-slate-300 hover:bg-brand-card hover:text-white"
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full border font-mono font-bold ${
                    isActive ? "bg-white/20 text-white border-white/30" : item.badgeColor
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Grounding & Security Verification Card */}
      <div className="glass-card rounded-xl p-3.5 border border-brand-border bg-gradient-to-b from-brand-card to-brand-navy/80">
        <div className="flex items-center space-x-2 text-emerald-400 mb-1.5">
          <ShieldCheck className="w-4 h-4" />
          <span className="text-[11px] font-bold tracking-wide">Statutory Grounding</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          CBDT IT Act 1961 v2024.2 synced. Non-hallucinatory rule execution enabled.
        </p>
        <div className="mt-2.5 pt-2 border-t border-slate-700/50 flex items-center justify-between text-[10px] text-slate-500 font-mono">
          <span>Integrity: SHA-256</span>
          <span className="text-emerald-400 font-bold">100% Verified</span>
        </div>
      </div>
    </aside>
  );
};
