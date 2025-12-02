"use client";

import { TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  trend: number;
  icon: React.ReactNode;
  iconBg: string;
  iconColor: string;
}

export default function MetricCard({
  title,
  value,
  trend,
  icon,
  iconBg,
  iconColor,
}: MetricCardProps) {
  const isPositive = trend >= 0;

  return (
    <div className="bg-white rounded-xl p-5 shadow-sm hover-lift border border-gray-100">
      <div className="flex items-start justify-between mb-4">
        <div className={`${iconBg} ${iconColor} p-3 rounded-lg`}>{icon}</div>
        <div
          className={`flex items-center gap-1 text-xs font-medium ${
            isPositive ? "text-green-positive" : "text-red-negative"
          }`}
        >
          {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          <span>{Math.abs(trend).toFixed(1)}%</span>
        </div>
      </div>
      <div>
        <p className="text-gray-600 text-xs font-medium mb-1 truncate">
          {title}
        </p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  );
}
