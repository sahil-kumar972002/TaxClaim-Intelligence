import React, { useState, useEffect } from "react";
import { Sliders, ShieldCheck, CheckCircle2, TrendingUp, AlertCircle, Info } from "lucide-react";
import { api } from "../../services/api";
import { SimulatorResponse } from "../../types";

export const WhatIfSimulator: React.FC = () => {
  const [grossReceipts, setGrossReceipts] = useState<number>(2400000);
  const [expenses, setExpenses] = useState<number>(850000);
  const [multiplier, setMultiplier] = useState<number>(0.90);
  const [simData, setSimData] = useState<SimulatorResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const runSimulation = async (receipts: number, exp: number, mult: number) => {
    setIsLoading(true);
    try {
      const res = await api.simulate({
        annual_gross_receipts: receipts,
        total_business_expenses: exp,
        business_use_multiplier: mult,
      });
      setSimData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    runSimulation(grossReceipts, expenses, multiplier);
  }, [grossReceipts, expenses, multiplier]);

  const sec44 = simData?.regimes["sec_44ada"];
  const pgbp = simData?.regimes["regular_pgbp"];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Sliders className="w-5 h-5 text-brand-primary" />
          <span>Tax What-If Simulator & Regime Comparator</span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Simulate statutory tax liability dynamically across Presumptive Scheme (Section 44ADA) vs Regular PGBP.
        </p>
      </div>

      {/* Interactive Sliders Panel */}
      <div className="glass-card rounded-2xl p-6 border border-brand-border space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Slider 1: Gross Receipts */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="font-bold text-slate-300">Annual Gross Receipts:</span>
              <span className="font-mono font-bold text-brand-accent text-sm">
                ₹{grossReceipts.toLocaleString("en-IN")}
              </span>
            </div>
            <input
              type="range"
              min="500000"
              max="7500000"
              step="100000"
              value={grossReceipts}
              onChange={(e) => setGrossReceipts(Number(e.target.value))}
              className="w-full accent-brand-primary cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>₹5 Lakhs</span>
              <span>Turnover Limit: ₹75L (Digital)</span>
            </div>
          </div>

          {/* Slider 2: Total Business Expenses */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="font-bold text-slate-300">Total Business Expenses:</span>
              <span className="font-mono font-bold text-emerald-400 text-sm">
                ₹{expenses.toLocaleString("en-IN")}
              </span>
            </div>
            <input
              type="range"
              min="100000"
              max="5000000"
              step="50000"
              value={expenses}
              onChange={(e) => setExpenses(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>₹1 Lakh</span>
              <span>₹50 Lakhs</span>
            </div>
          </div>

          {/* Slider 3: Business-Use Multiplier */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="font-bold text-slate-300">Business-Use Allocation:</span>
              <span className="font-mono font-bold text-brand-primary text-sm">
                {Math.round(multiplier * 100)}%
              </span>
            </div>
            <input
              type="range"
              min="0.50"
              max="1.0"
              step="0.05"
              value={multiplier}
              onChange={(e) => setMultiplier(Number(e.target.value))}
              className="w-full accent-brand-primary cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>50% (Shared Use)</span>
              <span>100% (Strict Business)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendation Banner */}
      {simData && (
        <div className="bg-gradient-to-r from-brand-primary/20 via-brand-card to-brand-accent/10 border border-brand-primary/40 rounded-2xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-glow">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-brand-accent px-2 py-0.5 rounded bg-brand-primary/20 border border-brand-accent/30">
              TaxClaim Recommendation
            </span>
            <h3 className="text-lg font-bold text-white mt-1.5 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span>Recommended: {simData.recommended_regime}</span>
            </h3>
            <p className="text-xs text-slate-300 mt-0.5">
              Filing under this regime provides an estimated statutory savings advantage.
            </p>
          </div>
          <div className="bg-brand-navy border border-brand-border rounded-xl px-4 py-2.5 text-right shrink-0">
            <div className="text-[11px] text-slate-400 font-medium">Estimated Tax Advantage</div>
            <div className="text-xl font-black text-emerald-400 font-mono">
              ₹{simData.potential_tax_savings.toLocaleString("en-IN")}
            </div>
          </div>
        </div>
      )}

      {/* Side-by-Side Regime Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card 1: Section 44ADA Presumptive */}
        <div className="glass-card rounded-2xl p-6 border border-brand-border space-y-4 relative">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Section 44ADA
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">
              Audit Exempt (≤ ₹75L)
            </span>
          </div>

          <div>
            <h4 className="text-base font-bold text-white">Presumptive Taxation for Professionals</h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Flat 50% deemed profit under Section 44ADA. No books of accounts required under Sec 44AA.
            </p>
          </div>

          <div className="bg-brand-navy/80 rounded-xl p-4 border border-brand-border space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Deemed Taxable Profit (50%):</span>
              <span className="font-mono font-bold text-white">
                ₹{sec44?.taxable_income.toLocaleString("en-IN")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Estimated Tax Payable:</span>
              <span className="font-mono font-bold text-emerald-400 text-sm">
                ₹{sec44?.estimated_tax_payable.toLocaleString("en-IN")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Effective Tax Rate:</span>
              <span className="font-mono text-slate-300">{sec44?.effective_tax_rate_percent}%</span>
            </div>
          </div>

          <div className="space-y-1.5 text-xs text-slate-300">
            <div className="font-bold text-[11px] text-slate-400 uppercase tracking-wider">Statutory Advantages:</div>
            <div className="flex items-center gap-1.5 text-emerald-300">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-400" />
              <span>Zero risk of expense disallowance during assessment</span>
            </div>
            <div className="flex items-center gap-1.5 text-emerald-300">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-400" />
              <span>Exempt from formal balance sheet / P&L maintenance</span>
            </div>
          </div>
        </div>

        {/* Card 2: Regular PGBP (Actual Expenses) */}
        <div className="glass-card rounded-2xl p-6 border border-brand-border space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Regular PGBP
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-bold">
              Books Required (Sec 44AA)
            </span>
          </div>

          <div>
            <h4 className="text-base font-bold text-white">Itemized Actual Expense Deductions</h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Gross receipts minus actual verified itemized business deductions under Section 37(1) & 32.
            </p>
          </div>

          <div className="bg-brand-navy/80 rounded-xl p-4 border border-brand-border space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Net Taxable Profit:</span>
              <span className="font-mono font-bold text-white">
                ₹{pgbp?.taxable_income.toLocaleString("en-IN")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Estimated Tax Payable:</span>
              <span className="font-mono font-bold text-emerald-400 text-sm">
                ₹{pgbp?.estimated_tax_payable.toLocaleString("en-IN")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Effective Tax Rate:</span>
              <span className="font-mono text-slate-300">{pgbp?.effective_tax_rate_percent}%</span>
            </div>
          </div>

          <div className="space-y-1.5 text-xs text-slate-300">
            <div className="font-bold text-[11px] text-slate-400 uppercase tracking-wider">Considerations:</div>
            <div className="flex items-center gap-1.5 text-slate-300">
              <Info className="w-3.5 h-3.5 shrink-0 text-brand-primary" />
              <span>Optimal if verified real costs exceed 50% of revenue</span>
            </div>
            <div className="flex items-center gap-1.5 text-amber-300">
              <AlertCircle className="w-3.5 h-3.5 shrink-0 text-amber-400" />
              <span>Requires complete receipt archives and proof of payment</span>
            </div>
          </div>
        </div>
      </div>

      {/* Legal Disclaimer */}
      <div className="text-[11px] text-slate-500 font-mono text-center pt-2">
        {simData?.disclaimer}
      </div>
    </div>
  );
};
