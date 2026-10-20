import React from "react";
import { Shield, Sparkles, AlertTriangle, FileText, CheckCircle2 } from "lucide-react";

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  currentProfession: string;
  onSelectProfession: (prof: string) => void;
  readinessScore: number;
}

const PROFESSIONS = [
  "Software Developer",
  "Graphic Designer",
  "Content Creator",
  "Uber / Ride Gig Worker",
  "Online STEM Tutor"
];

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  currentProfession,
  onSelectProfession,
  readinessScore
}) => {
  return (
    <header className="sticky top-0 z-50 glass-card border-b border-brand-border bg-brand-dark/90 backdrop-blur-md px-6 py-3.5 flex items-center justify-between">
      {/* Brand Identity */}
      <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("dashboard")}>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-primary to-brand-accent flex items-center justify-center shadow-glow">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-lg tracking-tight text-white">TaxClaim</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-primary/20 text-brand-accent border border-brand-accent/30 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-brand-accent" /> AI Intelligence
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-mono">Evidence-Backed Statutory Engine</p>
        </div>
      </div>

      {/* Center Persona Switcher */}
      <div className="hidden md:flex items-center bg-brand-navy/80 border border-brand-border rounded-xl p-1 shadow-inner">
        <span className="text-xs font-medium text-slate-400 px-3 py-1">Persona:</span>
        <select
          value={currentProfession}
          onChange={(e) => onSelectProfession(e.target.value)}
          className="bg-brand-card text-xs font-medium text-slate-200 border border-brand-border rounded-lg px-3 py-1.5 focus:outline-none focus:border-brand-primary cursor-pointer"
        >
          {PROFESSIONS.map((p) => (
            <option key={p} value={p}>
              {p} (CBDT FY 2024-25)
            </option>
          ))}
        </select>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Audit Readiness Pill */}
        <div className="hidden sm:flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 rounded-xl px-3 py-1.5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span className="text-xs font-medium text-slate-300">Audit Readiness:</span>
          <span className="text-xs font-bold text-emerald-400 font-mono">{readinessScore}%</span>
        </div>

        {/* Quick Action Buttons */}
        <button
          onClick={() => setActiveTab("ingestion")}
          className="px-3 py-1.5 rounded-xl bg-brand-primary hover:bg-brand-primaryHover text-white text-xs font-semibold shadow-glow flex items-center space-x-1.5 transition-all"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Upload Invoices</span>
        </button>

        <button
          onClick={() => setActiveTab("copilot")}
          className="px-3 py-1.5 rounded-xl bg-brand-card hover:bg-brand-cardHover border border-brand-border text-brand-accent text-xs font-semibold flex items-center space-x-1.5 transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Tax Copilot</span>
        </button>
      </div>
    </header>
  );
};
