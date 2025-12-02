"use client";

import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import { Download, RefreshCw, Filter } from "lucide-react";

type TrendPoint = {
  year: number;
  igs: number;
  place: number;
  economy: number;
  community: number;
};

export default function IGSTrendsPage() {
  const [data, setData] = useState<TrendPoint[]>([]);
  const [range, setRange] = useState<{ start: number; end: number }>({
    start: 2019,
    end: 2024,
  });
  const [movingAvg, setMovingAvg] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/igs-trends");
        const json = await res.json();
        setData(json.data || []);
      } catch (err) {
        console.error("Failed to fetch trends", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filtered = useMemo(() => {
    return data.filter((d) => d.year >= range.start && d.year <= range.end);
  }, [data, range]);

  const averaged = useMemo(() => {
    if (!movingAvg) return filtered;
    const arr = [...filtered];
    return arr.map((d, i) => {
      const w = 2; // 2-year window
      const slice = arr.slice(Math.max(0, i - w + 1), i + 1);
      const avg = (key: keyof TrendPoint) =>
        Number(
          (
            slice.reduce((s, p) => s + (p[key] as number), 0) / slice.length
          ).toFixed(2)
        );
      return {
        ...d,
        igs: avg("igs"),
        place: avg("place"),
        economy: avg("economy"),
        community: avg("community"),
      };
    });
  }, [filtered, movingAvg]);

  const summary = useMemo(() => {
    if (!filtered.length) return null;
    const first = filtered[0];
    const last = filtered[filtered.length - 1];
    const growth = (a: number, b: number) =>
      Number((((b - a) / a) * 100).toFixed(1));
    return {
      igs: {
        start: first.igs,
        end: last.igs,
        change: growth(first.igs, last.igs),
      },
      place: {
        start: first.place,
        end: last.place,
        change: growth(first.place, last.place),
      },
      economy: {
        start: first.economy,
        end: last.economy,
        change: growth(first.economy, last.economy),
      },
      community: {
        start: first.community,
        end: last.community,
        change: growth(first.community, last.community),
      },
    };
  }, [filtered]);

  const handleDownloadCSV = async () => {
    try {
      const res = await fetch("/api/igs-trends");
      const json = await res.json();
      const rows: TrendPoint[] = json.data || [];
      const header = "Year,IGS,Place,Economy,Community\n";
      const body = rows
        .map((r) => `${r.year},${r.igs},${r.place},${r.economy},${r.community}`)
        .join("\n");
      const blob = new Blob([header + body], {
        type: "text/csv;charset=utf-8;",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `IGS_Trends_${range.start}-${range.end}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error("CSV export failed", e);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-poppins font-bold text-gray-900">
            IGS Trends Analysis
          </h1>
          <p className="text-gray-600 mt-2">
            Historical trends and patterns in Inclusive Growth Score
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleDownloadCSV}
            className="px-3 py-2 bg-gray-900 text-white rounded-lg flex items-center gap-2 hover:bg-black"
          >
            <Download className="w-4 h-4" /> Export CSV
          </button>
          <button
            onClick={() => location.reload()}
            className="px-3 py-2 bg-gray-100 text-gray-800 rounded-lg flex items-center gap-2 hover:bg-gray-200"
          >
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <Filter className="w-4 h-4 text-gray-600" />
            <label className="text-sm text-gray-700">Year Range</label>
            <input
              type="number"
              value={range.start}
              onChange={(e) =>
                setRange((r) => ({ ...r, start: Number(e.target.value) }))
              }
              className="w-24 px-3 py-2 border rounded-lg"
            />
            <span className="text-gray-500">to</span>
            <input
              type="number"
              value={range.end}
              onChange={(e) =>
                setRange((r) => ({ ...r, end: Number(e.target.value) }))
              }
              className="w-24 px-3 py-2 border rounded-lg"
            />
          </div>
          <label className="inline-flex items-center gap-2">
            <input
              type="checkbox"
              checked={movingAvg}
              onChange={(e) => setMovingAvg(e.target.checked)}
            />
            <span className="text-sm text-gray-700">
              Apply 2-year moving average
            </span>
          </label>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-xl font-poppins font-semibold text-gray-900 mb-4">
            IGS and Pillar Trends
          </h3>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={averaged}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="year" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "white",
                  border: "1px solid #e5e7eb",
                  borderRadius: 8,
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="igs"
                stroke="#4C8DFF"
                strokeWidth={3}
                name="IGS"
              />
              <Line
                type="monotone"
                dataKey="place"
                stroke="#FF7A45"
                strokeWidth={2}
                name="Place"
              />
              <Line
                type="monotone"
                dataKey="economy"
                stroke="#6C63FF"
                strokeWidth={2}
                name="Economy"
              />
              <Line
                type="monotone"
                dataKey="community"
                stroke="#FFB800"
                strokeWidth={2}
                name="Community"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-xl font-poppins font-semibold text-gray-900 mb-4">
            IGS Distribution
          </h3>
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={averaged}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="year" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "white",
                  border: "1px solid #e5e7eb",
                  borderRadius: 8,
                }}
              />
              <Area
                type="monotone"
                dataKey="igs"
                stroke="#4C8DFF"
                fill="#4C8DFF"
                fillOpacity={0.15}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary */}
      {summary && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-xl font-poppins font-semibold text-gray-900 mb-6">
            Summary Statistics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {(["igs", "place", "economy", "community"] as const).map((k) => (
              <div
                key={k}
                className="p-4 rounded-lg border border-gray-200 bg-gray-50"
              >
                <p className="text-sm text-gray-600 mb-1 uppercase">{k}</p>
                <p className="text-xs text-gray-600">Start</p>
                <p className="text-xl font-bold text-gray-900">
                  {summary[k].start}
                </p>
                <p className="text-xs text-gray-600 mt-2">End</p>
                <p className="text-xl font-bold text-gray-900">
                  {summary[k].end}
                </p>
                <p className="text-xs text-gray-600 mt-2">Change</p>
                <p
                  className={`text-lg font-bold ${
                    summary[k].change >= 0 ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {summary[k].change}%
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
