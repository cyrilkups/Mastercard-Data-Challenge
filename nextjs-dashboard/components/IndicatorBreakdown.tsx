"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Cell,
} from "recharts";

const data = [
  { name: "Community", value: 40, color: "#FFB800" },
  { name: "Place", value: 21, color: "#FF7A45" },
  { name: "Economy", value: 20, color: "#6C63FF" },
];

export default function IndicatorBreakdown() {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 h-full">
      <div className="mb-6">
        <h3 className="text-xl font-poppins font-semibold text-gray-900">
          Pillar Breakdown
        </h3>
        <p className="text-sm text-gray-600 mt-1">Current scores by category</p>
      </div>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} layout="vertical">
          <XAxis type="number" domain={[0, 100]} stroke="#9CA3AF" />
          <YAxis type="category" dataKey="name" width={100} stroke="#9CA3AF" />
          <Bar dataKey="value" radius={[0, 8, 8, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-6 space-y-3">
        {data.map((item) => (
          <div key={item.name} className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: item.color }}
              ></div>
              <span className="text-sm text-gray-700">{item.name}</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
