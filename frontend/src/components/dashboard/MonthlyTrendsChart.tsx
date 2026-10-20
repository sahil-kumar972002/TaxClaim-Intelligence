import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

interface MonthlyTrendsChartProps {
  data: {
    month: string;
    total_expense: number;
    deductible: number;
    savings: number;
  }[];
}

export const MonthlyTrendsChart: React.FC<MonthlyTrendsChartProps> = ({ data }) => {
  return (
    <div className="glass-card rounded-2xl p-5 border border-brand-border h-[320px] flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-sm font-bold text-white">Monthly Expense & Deductible Trend</h3>
          <p className="text-[11px] text-slate-400">Total expenditure vs verified statutory deductions</p>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
            <span className="text-slate-400 text-[11px]">Total Expense</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-brand-primary"></span>
            <span className="text-brand-accent text-[11px] font-medium">Eligible Claims</span>
          </div>
        </div>
      </div>

      <div className="w-full h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorDeductible" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366F1" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#6366F1" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#475569" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#475569" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
            <XAxis dataKey="month" stroke="#64748B" fontSize={11} tickLine={false} />
            <YAxis
              stroke="#64748B"
              fontSize={11}
              tickLine={false}
              tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0F172A",
                borderColor: "#334155",
                borderRadius: "0.75rem",
                fontSize: "12px",
                color: "#F8FAFC",
              }}
              formatter={(value: any) => [`₹${Number(value).toLocaleString("en-IN")}`, ""]}
            />
            <Area
              type="monotone"
              dataKey="total_expense"
              stroke="#64748B"
              strokeWidth={1.5}
              fillOpacity={1}
              fill="url(#colorExpense)"
            />
            <Area
              type="monotone"
              dataKey="deductible"
              stroke="#6366F1"
              strokeWidth={2.5}
              fillOpacity={1}
              fill="url(#colorDeductible)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
