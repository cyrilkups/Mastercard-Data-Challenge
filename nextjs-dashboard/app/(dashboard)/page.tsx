"use client";

import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, Home, Briefcase, Users } from "lucide-react";
import MetricCard from "@/components/MetricCard";
import IGSTrendChart from "@/components/IGSTrendChart";
import IndicatorBreakdown from "@/components/IndicatorBreakdown";

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    igs: 58.03,
    place: 21,
    economy: 20,
    community: 40,
  });

  const [trends, setTrends] = useState({
    igs: 3.85,
    place: -5.2,
    economy: -2.7,
    community: 4.1,
  });

  // Simulate live updates every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics((prev) => ({
        igs: Math.max(0, Math.min(100, prev.igs + (Math.random() - 0.5) * 2)),
        place: Math.max(
          0,
          Math.min(100, prev.place + (Math.random() - 0.5) * 1.5)
        ),
        economy: Math.max(
          0,
          Math.min(100, prev.economy + (Math.random() - 0.5) * 1.5)
        ),
        community: Math.max(
          0,
          Math.min(100, prev.community + (Math.random() - 0.5) * 1.5)
        ),
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-poppins font-bold text-gray-900">
          Dashboard Overview
        </h1>
        <p className="text-gray-600 mt-2">
          Track and analyze Inclusive Growth Score metrics in real-time
        </p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="IGS Score"
          value={metrics.igs.toFixed(2)}
          trend={trends.igs}
          icon={<TrendingUp className="w-6 h-6" />}
          iconBg="bg-blue-100"
          iconColor="text-blue-metric"
        />
        <MetricCard
          title="Place Score"
          value={metrics.place.toFixed(0)}
          trend={trends.place}
          icon={<Home className="w-6 h-6" />}
          iconBg="bg-orange-100"
          iconColor="text-orange-metric"
        />
        <MetricCard
          title="Economy Score"
          value={metrics.economy.toFixed(0)}
          trend={trends.economy}
          icon={<Briefcase className="w-6 h-6" />}
          iconBg="bg-purple-100"
          iconColor="text-purple-primary"
        />
        <MetricCard
          title="Community Score"
          value={metrics.community.toFixed(0)}
          trend={trends.community}
          icon={<Users className="w-6 h-6" />}
          iconBg="bg-yellow-100"
          iconColor="text-gold-metric"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <IGSTrendChart />
        </div>
        <div>
          <IndicatorBreakdown />
        </div>
      </div>
    </div>
  );
}
