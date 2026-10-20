import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

interface CategoryDistributionProps {
  categories: Record<string, number>;
}

const COLORS = [
  "#6366F1", "#06B6D4", "#10B981", "#F59E0B",
  "#EC4899", "#8B5CF6", "#14B8A6", "#3B82F6"
];

export const CategoryDistribution: React.FC<CategoryDistributionProps> = ({ categories }) => {
  const data = Object.entries(categories).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value: Math.round(value),
  }));

  const total = data.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <div className="glass-card rounded-2xl p-5 border border-brand-border h-[320px] flex flex-col justify-between">
      <div>
        <h3 className="text-sm font-bold text-white">Expense Category Distribution</h3>
        <p className="text-[11px] text-slate-400">Proportional allocation of claimed deductions</p>
      </div>

      <div className="flex items-center justify-between">
        <div className="w-1/2 h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={75}
                paddingAngle={3}
                dataKey="value"
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0F172A",
                  borderColor: "#334155",
                  borderRadius: "0.5rem",
                  fontSize: "11px",
                  color: "#fff",
                }}
                formatter={(val: any) => [`₹${Number(val).toLocaleString("en-IN")}`, ""]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}
        <div className="w-1/2 space-y-1.5 max-h-[200px] overflow-y-auto pr-1">
          {data.slice(0, 6).map((item, idx) => {
            const pct = total > 0 ? Math.round((item.value / total) * 100) : 0;
            return (
              <div key={item.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2 truncate">
                  <span
                    className="w-2.5 h-2.5 rounded-full shrink-0"
                    style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                  ></span>
                  <span className="text-slate-300 truncate text-[11px]">{item.name}</span>
                </div>
                <span className="text-slate-400 font-mono text-[11px] font-medium">{pct}%</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
