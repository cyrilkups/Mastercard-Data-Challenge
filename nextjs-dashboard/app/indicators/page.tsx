"use client";

import { useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
  Area,
  AreaChart,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import {
  Search,
  SlidersHorizontal,
  X,
  TrendingUp,
  TrendingDown,
} from "lucide-react";

type Indicator = {
  name: string;
  value: number;
  trend: number;
  status: "good" | "warning" | "critical";
  unit: string;
  description: string;
  series: { year: string; value: number }[];
};

function sparkline(values: number[]): { year: string; value: number }[] {
  const years = ["2019", "2020", "2021", "2022", "2023", "2024"];
  return values.map((v, i) => ({ year: years[i], value: v }));
}

// Key Findings Chart Data
const broadbandData = [
  { year: 2019, tract: 44.1, arkansas: 76.2, usa: 83.1 },
  { year: 2020, tract: 45.7, arkansas: 77.8, usa: 84.2 },
  { year: 2021, tract: 45.8, arkansas: 79.1, usa: 85.0 },
  { year: 2022, tract: 53.2, arkansas: 80.5, usa: 86.1 },
  { year: 2023, tract: 58.7, arkansas: 81.8, usa: 86.8 },
  { year: 2024, tract: 58.7, arkansas: 82.7, usa: 87.3 },
];

const housingData = [
  { year: 2019, burden: 91.0, threshold: 30 },
  { year: 2020, burden: 89.5, threshold: 30 },
  { year: 2021, burden: 86.6, threshold: 30 },
  { year: 2022, burden: 87.0, threshold: 30 },
  { year: 2023, burden: 86.5, threshold: 30 },
  { year: 2024, burden: 86.5, threshold: 30 },
];

const incomeData = [
  { year: 2019, percentile: 36.9 },
  { year: 2020, percentile: 14.1 },
  { year: 2021, percentile: -2.9 },
  { year: 2022, percentile: -12.1 },
  { year: 2023, percentile: -15.6 },
  { year: 2024, percentile: -15.6 },
];

const povertyData = [
  { year: 2019, overall: 22.0, child: 27.0 },
  { year: 2020, overall: 23.0, child: 28.0 },
  { year: 2021, overall: 24.0, child: 29.0 },
  { year: 2022, overall: 24.5, child: 29.5 },
  { year: 2023, overall: 25.0, child: 30.0 },
  { year: 2024, overall: 25.0, child: 30.0 },
];

const educationData = [
  { year: 2019, tract: 50.0, ruralAvg: 44.2 },
  { year: 2020, tract: 47.0, ruralAvg: 43.8 },
  { year: 2021, tract: 43.5, ruralAvg: 43.5 },
  { year: 2022, tract: 40.0, ruralAvg: 43.0 },
  { year: 2023, tract: 36.7, ruralAvg: 42.7 },
  { year: 2024, tract: 33.4, ruralAvg: 42.5 },
];

type ChartType =
  | "broadband"
  | "housing"
  | "income"
  | "poverty"
  | "education"
  | null;

export default function IndicatorsPage() {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<"value" | "trend">("value");
  const [selectedIndicator, setSelectedIndicator] = useState<Indicator | null>(
    null
  );
  const [selectedFindingChart, setSelectedFindingChart] =
    useState<ChartType>(null);

  const indicators: Indicator[] = [
    {
      name: "Broadband Access",
      value: 58.7,
      trend: +14.6,
      status: "warning",
      unit: "%",
      description: "28.6pp below U.S. average (87.3%)",
      series: sparkline([44.1, 47.2, 51.0, 54.3, 56.5, 58.7]),
    },
    {
      name: "Housing Cost Burden",
      value: 86.5,
      trend: -4.5,
      status: "critical",
      unit: "%",
      description: "Households spending >30% on housing",
      series: sparkline([91.0, 90.2, 89.0, 88.0, 87.0, 86.5]),
    },
    {
      name: "Minority-Owned Business",
      value: 8.3,
      trend: +48.3,
      status: "good",
      unit: "%",
      description: "Recovery from -40% in 2019",
      series: sparkline([-40, -20, 0, 3.0, 6.0, 8.3]),
    },
    {
      name: "Early Education Enrollment",
      value: 33.4,
      trend: -16.6,
      status: "critical",
      unit: "%",
      description: "Children enrolled in early education",
      series: sparkline([50.0, 47.0, 43.0, 38.0, 35.0, 33.4]),
    },
    {
      name: "Median Income Percentile",
      value: -15.6,
      trend: -52.5,
      status: "critical",
      unit: "percentile",
      description: "Relative to state median income",
      series: sparkline([36.9, 25.0, 10.0, -5.0, -10.0, -15.6]),
    },
    {
      name: "Labor Force Participation",
      value: 67.0,
      trend: +4.0,
      status: "good",
      unit: "%",
      description: "Adults in workforce",
      series: sparkline([63.0, 64.0, 65.0, 66.0, 66.5, 67.0]),
    },
  ];

  const filtered = useMemo(() => {
    return indicators
      .filter((i) => i.name.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) =>
        sortKey === "value" ? b.value - a.value : b.trend - a.trend
      );
  }, [query, sortKey]);

  const renderFindingChartModal = () => {
    if (!selectedFindingChart) return null;

    const chartConfig: Record<
      string,
      { title: string; component: JSX.Element }
    > = {
      broadband: {
        title: "Broadband Access Trends (2019-2024)",
        component: (
          <LineChart data={broadbandData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[40, 90]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="tract"
              stroke="#ef4444"
              strokeWidth={3}
              name="Tract 20800"
            />
            <Line
              type="monotone"
              dataKey="arkansas"
              stroke="#3b82f6"
              strokeWidth={3}
              name="Arkansas"
            />
            <Line
              type="monotone"
              dataKey="usa"
              stroke="#22c55e"
              strokeWidth={3}
              name="USA"
            />
          </LineChart>
        ),
      },
      housing: {
        title: "Housing Cost Burden Over Time",
        component: (
          <AreaChart data={housingData}>
            <defs>
              <linearGradient id="colorBurdenModal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.2} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[0, 100]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="burden"
              stroke="#ef4444"
              fill="url(#colorBurdenModal)"
              name="Cost Burdened %"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="threshold"
              stroke="#22c55e"
              strokeWidth={3}
              strokeDasharray="5 5"
              name="Affordable Threshold"
            />
          </AreaChart>
        ),
      },
      income: {
        title: "Median Income Percentile Trends",
        component: (
          <AreaChart data={incomeData}>
            <defs>
              <linearGradient id="colorIncomeModal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.2} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[-20, 40]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="percentile"
              stroke="#ef4444"
              fill="url(#colorIncomeModal)"
              name="Income Percentile"
              strokeWidth={2}
            />
          </AreaChart>
        ),
      },
      poverty: {
        title: "Poverty Rates by Age Group",
        component: (
          <LineChart data={povertyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[15, 35]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="overall"
              stroke="#ef4444"
              strokeWidth={3}
              name="Overall Poverty"
            />
            <Line
              type="monotone"
              dataKey="child"
              stroke="#dc2626"
              strokeWidth={3}
              name="Child Poverty (<18)"
            />
          </LineChart>
        ),
      },
      education: {
        title: "Early Education Enrollment Comparison",
        component: (
          <LineChart data={educationData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[30, 55]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="tract"
              stroke="#ef4444"
              strokeWidth={3}
              name="Tract 20800"
            />
            <Line
              type="monotone"
              dataKey="ruralAvg"
              stroke="#22c55e"
              strokeWidth={3}
              name="Rural Average"
            />
          </LineChart>
        ),
      },
    };

    const config = chartConfig[selectedFindingChart];
    if (!config) return null;

    return (
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={() => setSelectedFindingChart(null)}
      >
        <div
          className="bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">{config.title}</h2>
            <button
              onClick={() => setSelectedFindingChart(null)}
              className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
            >
              ×
            </button>
          </div>
          <div className="p-6">
            <ResponsiveContainer width="100%" height={500}>
              {config.component}
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {renderFindingChartModal()}
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-poppins font-bold text-gray-900">
            Key Indicators
          </h1>
          <p className="text-gray-600 mt-2">
            Detailed analysis of indicators contributing to IGS
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg px-3 py-2">
            <Search className="w-4 h-4 text-gray-600" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search indicators"
              className="outline-none text-sm"
            />
          </div>
          <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg px-3 py-2">
            <SlidersHorizontal className="w-4 h-4 text-gray-600" />
            <select
              value={sortKey}
              onChange={(e) => setSortKey(e.target.value as any)}
              className="text-sm"
            >
              <option value="value">Sort by Value</option>
              <option value="trend">Sort by Trend</option>
            </select>
          </div>
        </div>
      </div>

      {/* Grid of indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((ind) => {
          const statusColors = {
            good: "bg-green-50 border-green-200",
            warning: "bg-yellow-50 border-yellow-200",
            critical: "bg-red-50 border-red-200",
          };

          return (
            <div
              key={ind.name}
              className={`rounded-xl p-5 shadow-sm border-2 ${
                statusColors[ind.status]
              } cursor-pointer hover:shadow-lg transition-all duration-200 hover:scale-[1.02]`}
              onClick={() => setSelectedIndicator(ind)}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-700">
                    {ind.name}
                  </p>
                  <div className="flex items-baseline gap-2 mt-1">
                    <p className="text-3xl font-bold text-gray-900">
                      {ind.value > 0 || ind.value === 0 ? ind.value : ind.value}
                      <span className="text-lg text-gray-600 ml-1">
                        {ind.unit}
                      </span>
                    </p>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    {ind.description}
                  </p>
                </div>
                <div
                  className={`px-3 py-1 rounded-md text-xs font-bold whitespace-nowrap ${
                    ind.trend >= 0
                      ? "bg-green-100 text-green-800 border border-green-300"
                      : "bg-red-100 text-red-800 border border-red-300"
                  }`}
                >
                  {ind.trend >= 0 ? "↑" : "↓"} {Math.abs(ind.trend).toFixed(1)}%
                </div>
              </div>

              <div className="mt-4 h-24 bg-white rounded-lg p-2">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={ind.series}>
                    <XAxis
                      dataKey="year"
                      tick={{ fontSize: 10, fill: "#6B7280" }}
                      stroke="#D1D5DB"
                    />
                    <YAxis
                      tick={{ fontSize: 10, fill: "#6B7280" }}
                      stroke="#D1D5DB"
                      width={40}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "white",
                        border: "1px solid #e5e7eb",
                        borderRadius: 8,
                        fontSize: 12,
                      }}
                      formatter={(value: any) => [
                        `${value}${ind.unit}`,
                        ind.name,
                      ]}
                      labelFormatter={(label) => `Year: ${label}`}
                    />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke={ind.trend >= 0 ? "#10B981" : "#EF4444"}
                      strokeWidth={3}
                      dot={{
                        fill: ind.trend >= 0 ? "#10B981" : "#EF4444",
                        r: 4,
                      }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          );
        })}
      </div>

      {/* Aggregate chart */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-xl font-poppins font-semibold text-gray-900 mb-4">
          Top Indicators by Value
        </h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={filtered}>
              <XAxis
                dataKey="name"
                stroke="#9CA3AF"
                tick={{ fontSize: 12 }}
                interval={0}
                height={60}
                angle={-20}
                dy={20}
              />
              <YAxis stroke="#9CA3AF" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "white",
                  border: "1px solid #e5e7eb",
                  borderRadius: 8,
                }}
              />
              <Bar dataKey="value" fill="#6C63FF" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Key Findings Section */}
      <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Key Findings: Detailed Analysis
        </h2>
        <p className="text-gray-600 mb-6">
          Click on any chart to view expanded analysis
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Broadband Chart */}
          <div
            onClick={() => setSelectedFindingChart("broadband")}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          >
            <h3 className="font-semibold text-gray-900 mb-3 text-sm">
              Broadband Access
            </h3>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={broadbandData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="year"
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <YAxis
                  domain={[40, 90]}
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="tract"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Tract"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="usa"
                  stroke="#22c55e"
                  strokeWidth={2}
                  name="USA"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-600 mt-2">
              28.6pp below U.S. average
            </p>
          </div>

          {/* Housing Chart */}
          <div
            onClick={() => setSelectedFindingChart("housing")}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          >
            <h3 className="font-semibold text-gray-900 mb-3 text-sm">
              Housing Cost Burden
            </h3>
            <ResponsiveContainer width="100%" height={150}>
              <AreaChart data={housingData}>
                <defs>
                  <linearGradient
                    id="colorBurdenSmall"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0.2} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="year"
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <YAxis
                  domain={[0, 100]}
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="burden"
                  stroke="#ef4444"
                  fill="url(#colorBurdenSmall)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-600 mt-2">
              86.5% cost-burdened households
            </p>
          </div>

          {/* Income Chart */}
          <div
            onClick={() => setSelectedFindingChart("income")}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          >
            <h3 className="font-semibold text-gray-900 mb-3 text-sm">
              Median Income
            </h3>
            <ResponsiveContainer width="100%" height={150}>
              <AreaChart data={incomeData}>
                <defs>
                  <linearGradient
                    id="colorIncomeSmall"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0.2} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="year"
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <YAxis
                  domain={[-20, 40]}
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="percentile"
                  stroke="#ef4444"
                  fill="url(#colorIncomeSmall)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-600 mt-2">
              -52.5 percentile point decline
            </p>
          </div>

          {/* Poverty Chart */}
          <div
            onClick={() => setSelectedFindingChart("poverty")}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          >
            <h3 className="font-semibold text-gray-900 mb-3 text-sm">
              Poverty Rates
            </h3>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={povertyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="year"
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <YAxis
                  domain={[15, 35]}
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="overall"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Overall"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="child"
                  stroke="#dc2626"
                  strokeWidth={2}
                  name="Child"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-600 mt-2">Child poverty ~30%</p>
          </div>

          {/* Education Chart */}
          <div
            onClick={() => setSelectedFindingChart("education")}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          >
            <h3 className="font-semibold text-gray-900 mb-3 text-sm">
              Early Education
            </h3>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={educationData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="year"
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <YAxis
                  domain={[30, 55]}
                  stroke="#6b7280"
                  tick={{ fontSize: 10 }}
                />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="tract"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Tract"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="ruralAvg"
                  stroke="#22c55e"
                  strokeWidth={2}
                  name="Rural Avg"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-600 mt-2">
              -16.6pp decline since 2019
            </p>
          </div>
        </div>
      </div>

      {/* Detailed Modal */}
      {selectedIndicator && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedIndicator(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-auto"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-start justify-between rounded-t-2xl">
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {selectedIndicator.name}
                </h2>
                <p className="text-gray-600">{selectedIndicator.description}</p>
                <div className="flex items-center gap-4 mt-3">
                  <div className="flex items-center gap-2">
                    {selectedIndicator.trend >= 0 ? (
                      <TrendingUp className="w-5 h-5 text-green-600" />
                    ) : (
                      <TrendingDown className="w-5 h-5 text-red-600" />
                    )}
                    <span
                      className={`text-lg font-bold ${
                        selectedIndicator.trend >= 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {selectedIndicator.trend >= 0 ? "+" : ""}
                      {selectedIndicator.trend.toFixed(1)}%
                    </span>
                    <span className="text-sm text-gray-600">since 2019</span>
                  </div>
                  <div className="h-6 w-px bg-gray-300" />
                  <div>
                    <span className="text-3xl font-bold text-gray-900">
                      {selectedIndicator.value}
                    </span>
                    <span className="text-lg text-gray-600 ml-1">
                      {selectedIndicator.unit}
                    </span>
                    <span className="text-sm text-gray-500 ml-2">(2024)</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setSelectedIndicator(null)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-6 h-6 text-gray-600" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-6">
              {/* Large Area Chart */}
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Trend Analysis (2019-2024)
                </h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={selectedIndicator.series}>
                      <defs>
                        <linearGradient
                          id="colorValue"
                          x1="0"
                          y1="0"
                          x2="0"
                          y2="1"
                        >
                          <stop
                            offset="5%"
                            stopColor={
                              selectedIndicator.trend >= 0
                                ? "#10B981"
                                : "#EF4444"
                            }
                            stopOpacity={0.3}
                          />
                          <stop
                            offset="95%"
                            stopColor={
                              selectedIndicator.trend >= 0
                                ? "#10B981"
                                : "#EF4444"
                            }
                            stopOpacity={0}
                          />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                      <XAxis
                        dataKey="year"
                        tick={{ fontSize: 14, fill: "#4B5563" }}
                        stroke="#9CA3AF"
                      />
                      <YAxis
                        tick={{ fontSize: 14, fill: "#4B5563" }}
                        stroke="#9CA3AF"
                        label={{
                          value: selectedIndicator.unit,
                          angle: -90,
                          position: "insideLeft",
                          style: { fontSize: 14, fill: "#6B7280" },
                        }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "white",
                          border: "2px solid #e5e7eb",
                          borderRadius: 12,
                          fontSize: 14,
                          padding: 12,
                        }}
                        formatter={(value: any) => [
                          `${value}${selectedIndicator.unit}`,
                          selectedIndicator.name,
                        ]}
                        labelFormatter={(label) => `Year: ${label}`}
                      />
                      <Area
                        type="monotone"
                        dataKey="value"
                        stroke={
                          selectedIndicator.trend >= 0 ? "#10B981" : "#EF4444"
                        }
                        strokeWidth={3}
                        fill="url(#colorValue)"
                        dot={{
                          fill:
                            selectedIndicator.trend >= 0
                              ? "#10B981"
                              : "#EF4444",
                          r: 6,
                          strokeWidth: 2,
                          stroke: "#fff",
                        }}
                        activeDot={{ r: 8 }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Statistics Grid */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-700 font-medium mb-1">
                    Starting Value
                  </p>
                  <p className="text-2xl font-bold text-blue-900">
                    {selectedIndicator.series[0].value}
                    {selectedIndicator.unit}
                  </p>
                  <p className="text-xs text-blue-600 mt-1">2019</p>
                </div>
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <p className="text-sm text-purple-700 font-medium mb-1">
                    Current Value
                  </p>
                  <p className="text-2xl font-bold text-purple-900">
                    {selectedIndicator.value}
                    {selectedIndicator.unit}
                  </p>
                  <p className="text-xs text-purple-600 mt-1">2024</p>
                </div>
                <div
                  className={`${
                    selectedIndicator.trend >= 0
                      ? "bg-green-50 border-green-200"
                      : "bg-red-50 border-red-200"
                  } border rounded-lg p-4`}
                >
                  <p
                    className={`text-sm font-medium mb-1 ${
                      selectedIndicator.trend >= 0
                        ? "text-green-700"
                        : "text-red-700"
                    }`}
                  >
                    Total Change
                  </p>
                  <p
                    className={`text-2xl font-bold ${
                      selectedIndicator.trend >= 0
                        ? "text-green-900"
                        : "text-red-900"
                    }`}
                  >
                    {selectedIndicator.trend >= 0 ? "+" : ""}
                    {selectedIndicator.trend.toFixed(1)}%
                  </p>
                  <p
                    className={`text-xs mt-1 ${
                      selectedIndicator.trend >= 0
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    6-year trend
                  </p>
                </div>
              </div>

              {/* Year-over-Year Changes */}
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Year-over-Year Changes
                </h3>
                <div className="space-y-2">
                  {selectedIndicator.series.slice(1).map((point, idx) => {
                    const prevValue = selectedIndicator.series[idx].value;
                    const change = point.value - prevValue;
                    const changePercent = (change / Math.abs(prevValue)) * 100;

                    return (
                      <div
                        key={point.year}
                        className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200"
                      >
                        <span className="font-medium text-gray-900">
                          {point.year}
                        </span>
                        <div className="flex items-center gap-4">
                          <span className="text-gray-600">
                            {prevValue}
                            {selectedIndicator.unit} → {point.value}
                            {selectedIndicator.unit}
                          </span>
                          <span
                            className={`font-bold ${
                              change >= 0 ? "text-green-600" : "text-red-600"
                            }`}
                          >
                            {change >= 0 ? "+" : ""}
                            {change.toFixed(1)}
                            {selectedIndicator.unit}
                            <span className="text-sm ml-1">
                              ({changePercent >= 0 ? "+" : ""}
                              {changePercent.toFixed(1)}%)
                            </span>
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
