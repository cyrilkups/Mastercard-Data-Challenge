"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { year: "2019", igs: 51.2, place: 26.5, economy: 22.8, community: 35.3 },
  { year: "2020", igs: 52.8, place: 25.1, economy: 21.5, community: 37.2 },
  { year: "2021", igs: 54.5, place: 23.8, economy: 20.9, community: 38.6 },
  { year: "2022", igs: 55.9, place: 22.4, economy: 20.3, community: 39.4 },
  { year: "2023", igs: 56.8, place: 21.7, economy: 20.1, community: 39.8 },
  { year: "2024", igs: 58.03, place: 21.0, economy: 20.0, community: 40.0 },
];

export default function IGSTrendChart() {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="mb-6">
        <h3 className="text-xl font-poppins font-semibold text-gray-900">
          IGS Trends Over Time
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          Historical performance across all pillars (2019-2024)
        </p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="year" stroke="#9CA3AF" />
          <YAxis stroke="#9CA3AF" />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="igs"
            stroke="#4C8DFF"
            strokeWidth={3}
            name="IGS Score"
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
  );
}
