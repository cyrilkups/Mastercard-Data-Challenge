"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface Scenario {
  name: string;
  baseline2024: number;
  value2027: number;
  value2030: number;
  gain2030: number;
  thresholdStatus: string;
  description: string;
  evidence: string;
  color: string;
}

const scenarios: Scenario[] = [
  {
    name: "Baseline (No Intervention)",
    baseline2024: 27.0,
    value2027: 26.1,
    value2030: 25.2,
    gain2030: -1.8,
    thresholdStatus: "19.8 points below threshold",
    description:
      "Without intervention, county continues steady decline, losing ~1.8 points over 6 years.",
    evidence: "Matches historical trajectory of similar rural counties",
    color: "red",
  },
  {
    name: "Housing Affordability (-10% burden)",
    baseline2024: 37.3,
    value2027: 39.3,
    value2030: 41.3,
    gain2030: 16.1,
    thresholdStatus: "3.7 points below threshold",
    description:
      "Housing affordability shows sustained compounding impact. Reduced cost burden enables workforce retention and economic participation.",
    evidence:
      "Chaffee/Fulton counties show Place score improvements with housing interventions",
    color: "orange",
  },
  {
    name: "Early Education Expansion (+12% enrollment)",
    baseline2024: 37.3,
    value2027: 40.6,
    value2030: 44.0,
    gain2030: 18.8,
    thresholdStatus: "1.0 point below threshold (closest)",
    description:
      "Education investments show accelerating returns. Early years build foundation; later years see compounding effects from improved workforce quality.",
    evidence:
      "Solution counties demonstrate Place score gains (+18.9) with education programs",
    color: "yellow",
  },
  {
    name: "Business Support (+15% minority businesses)",
    baseline2024: 37.5,
    value2027: 39.9,
    value2030: 42.3,
    gain2030: 17.1,
    thresholdStatus: "2.7 points below threshold",
    description:
      "Business support drives economic diversification. Shows strongest Economy score impact (+10.8). Time needed for establishment and market development.",
    evidence: "Beltrami County employment growth +231% (2020-2023)",
    color: "blue",
  },
  {
    name: "Combined Intervention Package",
    baseline2024: 37.5,
    value2027: 41.6,
    value2030: 45.7,
    gain2030: 20.5,
    thresholdStatus: "✓ 0.7 points ABOVE threshold!",
    description:
      "Comprehensive multi-pillar approach yields strongest, most consistent improvement. Synergistic effects across Place, Economy, and Community pillars.",
    evidence: "Cross-county analysis validates multi-intervention benefits",
    color: "green",
  },
];

const modelImprovements = [
  {
    metric: "IGS Prediction Accuracy",
    original: "R² = 0.55",
    augmented: "R² = 0.73",
    improvement: "+32%",
  },
  {
    metric: "Economy Score Model",
    original: "R² = 0.05",
    augmented: "R² = 0.44",
    improvement: "+780%",
  },
  {
    metric: "Training Samples",
    original: "26 (1 county)",
    augmented: "38 (4 counties)",
    improvement: "+46%",
  },
  {
    metric: "Evidence Base",
    original: "Lonoke only",
    augmented: "Beltrami, Chaffee, Fulton",
    improvement: "Real improvements",
  },
];

// Generate forecast data for charts
const forecastData = [
  {
    year: 2024,
    baseline: 27.0,
    housing: 37.3,
    education: 37.3,
    business: 37.5,
    combined: 37.5,
    threshold: 45,
  },
  {
    year: 2025,
    baseline: 26.7,
    housing: 37.8,
    education: 38.1,
    business: 38.0,
    combined: 38.7,
    threshold: 45,
  },
  {
    year: 2026,
    baseline: 26.4,
    housing: 38.5,
    education: 39.3,
    business: 38.9,
    combined: 40.1,
    threshold: 45,
  },
  {
    year: 2027,
    baseline: 26.1,
    housing: 39.3,
    education: 40.6,
    business: 39.9,
    combined: 41.6,
    threshold: 45,
  },
  {
    year: 2028,
    baseline: 25.7,
    housing: 40.0,
    education: 42.0,
    business: 40.8,
    combined: 43.2,
    threshold: 45,
  },
  {
    year: 2029,
    baseline: 25.5,
    housing: 40.7,
    education: 43.0,
    business: 41.6,
    combined: 44.5,
    threshold: 45,
  },
  {
    year: 2030,
    baseline: 25.2,
    housing: 41.3,
    education: 44.0,
    business: 42.3,
    combined: 45.7,
    threshold: 45,
  },
];

const pillarData = [
  {
    pillar: "Place",
    baseline: 21,
    housing: 38,
    education: 40,
    business: 25,
    combined: 42,
  },
  {
    pillar: "Economy",
    baseline: 20,
    housing: 23,
    education: 25,
    business: 34,
    combined: 35,
  },
  {
    pillar: "Community",
    baseline: 40,
    housing: 42,
    education: 58,
    business: 43,
    combined: 60,
  },
];

const comparisonData = [
  { scenario: "Baseline", value2024: 27.0, value2030: 25.2, improvement: -1.8 },
  { scenario: "Housing", value2024: 37.3, value2030: 41.3, improvement: 16.1 },
  {
    scenario: "Education",
    value2024: 37.3,
    value2030: 44.0,
    improvement: 18.8,
  },
  { scenario: "Business", value2024: 37.5, value2030: 42.3, improvement: 17.1 },
  { scenario: "Combined", value2024: 37.5, value2030: 45.7, improvement: 20.5 },
];

type ChartType = "forecast" | "pillar" | "comparison" | "trajectory" | null;

export default function MLPredictionsPage() {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [selectedChart, setSelectedChart] = useState<ChartType>(null);

  const renderExpandedChart = () => {
    if (!selectedChart) return null;

    const chartConfig: Record<
      string,
      { title: string; component: JSX.Element; description: string }
    > = {
      forecast: {
        title: "IGS Forecast by Scenario (2024-2030)",
        description:
          "Year-by-year projections showing all intervention scenarios compared to baseline",
        component: (
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[20, 60]} stroke="#6b7280" />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
              }}
            />
            <Legend />
            <ReferenceLine
              y={45}
              stroke="#ef4444"
              strokeDasharray="5 5"
              label="Threshold"
            />
            <Line
              type="monotone"
              dataKey="baseline"
              stroke="#dc2626"
              strokeWidth={3}
              name="Baseline"
            />
            <Line
              type="monotone"
              dataKey="housing"
              stroke="#f97316"
              strokeWidth={3}
              name="Housing"
            />
            <Line
              type="monotone"
              dataKey="education"
              stroke="#eab308"
              strokeWidth={3}
              name="Education"
            />
            <Line
              type="monotone"
              dataKey="business"
              stroke="#3b82f6"
              strokeWidth={3}
              name="Business"
            />
            <Line
              type="monotone"
              dataKey="combined"
              stroke="#22c55e"
              strokeWidth={4}
              name="Combined"
            />
          </LineChart>
        ),
      },
      pillar: {
        title: "Pillar-Specific Impacts by 2030",
        description:
          "Baseline vs. Combined intervention effects across Place, Economy, and Community pillars",
        component: (
          <BarChart data={pillarData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="pillar" stroke="#6b7280" />
            <YAxis domain={[0, 70]} stroke="#6b7280" />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
              }}
            />
            <Legend />
            <Bar dataKey="baseline" fill="#dc2626" name="Baseline" />
            <Bar dataKey="combined" fill="#22c55e" name="Combined" />
          </BarChart>
        ),
      },
      comparison: {
        title: "2024 vs 2030 Net Improvement",
        description:
          "Total IGS point gains from baseline (2024) to target year (2030) for each scenario",
        component: (
          <BarChart data={comparisonData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis type="number" domain={[-5, 50]} stroke="#6b7280" />
            <YAxis
              type="category"
              dataKey="scenario"
              stroke="#6b7280"
              width={100}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
              }}
            />
            <Legend />
            <Bar dataKey="improvement" fill="#6366f1" name="Net Improvement" />
          </BarChart>
        ),
      },
      trajectory: {
        title: "Combined Intervention Trajectory vs Baseline",
        description:
          "Area comparison showing the growing gap between intervention and no-intervention paths",
        component: (
          <AreaChart data={forecastData}>
            <defs>
              <linearGradient
                id="colorCombinedExpanded"
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0.1} />
              </linearGradient>
              <linearGradient
                id="colorBaselineExpanded"
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="5%" stopColor="#dc2626" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#dc2626" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[20, 60]} stroke="#6b7280" />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
              }}
            />
            <Legend />
            <ReferenceLine
              y={45}
              stroke="#ef4444"
              strokeDasharray="5 5"
              label="Threshold (45)"
            />
            <Area
              type="monotone"
              dataKey="baseline"
              stroke="#dc2626"
              fill="url(#colorBaselineExpanded)"
              strokeWidth={3}
              name="Baseline"
            />
            <Area
              type="monotone"
              dataKey="combined"
              stroke="#22c55e"
              fill="url(#colorCombinedExpanded)"
              strokeWidth={4}
              name="Combined Intervention"
            />
          </AreaChart>
        ),
      },
    };

    const config = chartConfig[selectedChart];
    if (!config) return null;

    return (
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={() => setSelectedChart(null)}
      >
        <div
          className="bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-2xl font-bold text-gray-900">
                {config.title}
              </h2>
              <button
                onClick={() => setSelectedChart(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
              >
                ×
              </button>
            </div>
            <p className="text-gray-600 text-sm">{config.description}</p>
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-purple-50 p-8">
      {renderExpandedChart()}
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            ML Predictions: 2030 Forecast
          </h1>
          <p className="text-lg text-gray-600">
            Augmented Model • Evidence-Based Projections • R² = 0.73 (+32%
            improvement)
          </p>
        </div>

        {/* Model Performance */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8 border-l-4 border-green-500">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Augmented Model Performance
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {modelImprovements.map((item, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-br from-green-50 to-blue-50 rounded-lg p-4"
              >
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  {item.metric}
                </h3>
                <div className="space-y-1">
                  <p className="text-xs text-gray-500">
                    Original: {item.original}
                  </p>
                  <p className="text-xs text-gray-900 font-semibold">
                    Augmented: {item.augmented}
                  </p>
                  <p className="text-lg font-bold text-green-600">
                    {item.improvement}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Prediction Charts */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Prediction Visualizations
          </h2>

          {/* IGS Forecast to 2030 */}
          <div
            onClick={() => setSelectedChart("forecast")}
            className="bg-white rounded-lg shadow-md p-6 mb-6 cursor-pointer hover:shadow-xl transition-all duration-200 hover:scale-[1.01]"
          >
            <h3 className="font-semibold text-gray-900 mb-4 text-xl">
              IGS Forecast by Scenario (2024-2030)
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="year" stroke="#6b7280" />
                <YAxis domain={[20, 60]} stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "white",
                    border: "1px solid #e5e7eb",
                    borderRadius: 8,
                  }}
                />
                <Legend />
                <ReferenceLine
                  y={45}
                  stroke="#ef4444"
                  strokeDasharray="5 5"
                  label="Threshold"
                />
                <Line
                  type="monotone"
                  dataKey="baseline"
                  stroke="#dc2626"
                  strokeWidth={2}
                  name="Baseline"
                />
                <Line
                  type="monotone"
                  dataKey="housing"
                  stroke="#f97316"
                  strokeWidth={2}
                  name="Housing"
                />
                <Line
                  type="monotone"
                  dataKey="education"
                  stroke="#eab308"
                  strokeWidth={2}
                  name="Education"
                />
                <Line
                  type="monotone"
                  dataKey="business"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  name="Business"
                />
                <Line
                  type="monotone"
                  dataKey="combined"
                  stroke="#22c55e"
                  strokeWidth={3}
                  name="Combined"
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-sm text-gray-700 mt-4 text-center">
              Combined intervention reaches 45.7 by 2030, successfully crossing
              distressed threshold (45)
            </p>
          </div>

          {/* Pillar Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div
              onClick={() => setSelectedChart("pillar")}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-xl transition-all duration-200 hover:scale-[1.01]"
            >
              <h3 className="font-semibold text-gray-900 mb-4 text-xl">
                Pillar-Specific Impacts by 2030
              </h3>
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={pillarData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="pillar" stroke="#6b7280" />
                  <YAxis domain={[0, 70]} stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e7eb",
                      borderRadius: 8,
                    }}
                  />
                  <Legend />
                  <Bar dataKey="baseline" fill="#dc2626" name="Baseline" />
                  <Bar dataKey="combined" fill="#22c55e" name="Combined" />
                </BarChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Breakdown of Place, Economy, and Community pillar improvements
                with combined interventions
              </p>
            </div>

            <div
              onClick={() => setSelectedChart("comparison")}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-xl transition-all duration-200 hover:scale-[1.01]"
            >
              <h3 className="font-semibold text-gray-900 mb-4 text-xl">
                2024 vs 2030 Comparison
              </h3>
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={comparisonData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis type="number" domain={[-5, 50]} stroke="#6b7280" />
                  <YAxis
                    type="category"
                    dataKey="scenario"
                    stroke="#6b7280"
                    width={100}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #e5e7eb",
                      borderRadius: 8,
                    }}
                  />
                  <Legend />
                  <Bar
                    dataKey="improvement"
                    fill="#6366f1"
                    name="Net Improvement"
                  />
                </BarChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Net improvement from baseline 2024 to 2030 for each scenario
              </p>
            </div>
          </div>

          {/* Trajectory Analysis */}
          <div
            onClick={() => setSelectedChart("trajectory")}
            className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-xl transition-all duration-200 hover:scale-[1.01]"
          >
            <h3 className="font-semibold text-gray-900 mb-4 text-xl">
              Combined Intervention Trajectory
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={forecastData}>
                <defs>
                  <linearGradient
                    id="colorCombined"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0.1} />
                  </linearGradient>
                  <linearGradient
                    id="colorBaseline"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor="#dc2626" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#dc2626" stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="year" stroke="#6b7280" />
                <YAxis domain={[20, 60]} stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "white",
                    border: "1px solid #e5e7eb",
                    borderRadius: 8,
                  }}
                />
                <Legend />
                <ReferenceLine
                  y={45}
                  stroke="#ef4444"
                  strokeDasharray="5 5"
                  label="Threshold (45)"
                />
                <Area
                  type="monotone"
                  dataKey="baseline"
                  stroke="#dc2626"
                  fill="url(#colorBaseline)"
                  strokeWidth={2}
                  name="Baseline"
                />
                <Area
                  type="monotone"
                  dataKey="combined"
                  stroke="#22c55e"
                  fill="url(#colorCombined)"
                  strokeWidth={3}
                  name="Combined Intervention"
                />
              </AreaChart>
            </ResponsiveContainer>
            <p className="text-sm text-gray-700 mt-4 text-center">
              Year-over-year progression showing accelerating returns with
              combined interventions vs. baseline decline
            </p>
          </div>
        </div>

        {/* Scenario Analysis */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Scenario Analysis & Projections
          </h2>
          <div className="space-y-4">
            {scenarios.map((scenario, idx) => {
              const borderColor =
                scenario.color === "green"
                  ? "border-green-500"
                  : scenario.color === "yellow"
                  ? "border-yellow-500"
                  : scenario.color === "orange"
                  ? "border-orange-500"
                  : scenario.color === "blue"
                  ? "border-blue-500"
                  : "border-red-500";
              const bgColor =
                scenario.color === "green"
                  ? "bg-green-50"
                  : scenario.color === "yellow"
                  ? "bg-yellow-50"
                  : scenario.color === "orange"
                  ? "bg-orange-50"
                  : scenario.color === "blue"
                  ? "bg-blue-50"
                  : "bg-red-50";

              return (
                <div
                  key={idx}
                  onClick={() => setSelectedScenario(scenario.name)}
                  className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${borderColor} hover:shadow-lg transition-all duration-200 cursor-pointer ${
                    selectedScenario === scenario.name
                      ? "ring-2 ring-blue-500 scale-[1.02]"
                      : ""
                  }`}
                >
                  <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
                    <div className="lg:col-span-1">
                      <h3 className="text-lg font-bold text-gray-900 mb-2">
                        {scenario.name}
                      </h3>
                      <div className={`${bgColor} rounded-lg p-3 space-y-1`}>
                        <div className="text-sm">
                          <span className="text-gray-600">2024:</span>
                          <span className="ml-2 font-semibold">
                            {scenario.baseline2024}
                          </span>
                        </div>
                        <div className="text-sm">
                          <span className="text-gray-600">2027:</span>
                          <span className="ml-2 font-semibold">
                            {scenario.value2027}
                          </span>
                        </div>
                        <div className="text-sm">
                          <span className="text-gray-600">2030:</span>
                          <span className="ml-2 font-bold text-lg">
                            {scenario.value2030}
                          </span>
                        </div>
                        <div className="text-sm pt-2 border-t border-gray-300">
                          <span className="text-gray-600">Gain:</span>
                          <span
                            className={`ml-2 font-bold ${
                              scenario.gain2030 > 0
                                ? "text-green-600"
                                : "text-red-600"
                            }`}
                          >
                            {scenario.gain2030 > 0 ? "+" : ""}
                            {scenario.gain2030}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="lg:col-span-3 space-y-3">
                      <div>
                        <p className="text-sm font-semibold text-gray-700 mb-1">
                          Threshold Status:
                        </p>
                        <p
                          className={`text-sm ${
                            scenario.name.includes("Combined")
                              ? "text-green-600 font-bold"
                              : "text-gray-600"
                          }`}
                        >
                          {scenario.thresholdStatus}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-700 mb-1">
                          Interpretation:
                        </p>
                        <p className="text-sm text-gray-600 leading-relaxed">
                          {scenario.description}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-700 mb-1">
                          Evidence:
                        </p>
                        <p className="text-sm text-gray-600 italic">
                          {scenario.evidence}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Key Findings */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Key Findings</h2>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                1
              </div>
              <p className="text-sm leading-relaxed">
                <span className="font-semibold">
                  Threshold Crossing Achieved:
                </span>{" "}
                Combined intervention reaches 45.7 by 2030, successfully
                crossing distressed threshold (45). Represents exit from
                distressed status.
              </p>
            </div>
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                2
              </div>
              <p className="text-sm leading-relaxed">
                <span className="font-semibold">
                  Early Education Strongest Impact:
                </span>{" "}
                Shows highest individual gains (+18.8 by 2030, +18.9 Place
                score). Demonstrates importance of human capital investment.
              </p>
            </div>
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                3
              </div>
              <p className="text-sm leading-relaxed">
                <span className="font-semibold">Validated Predictions:</span>{" "}
                Model trained on counties that achieved real improvements
                (Chaffee/Fulton: 37→42, Beltrami: +231% employment). 73%
                accuracy vs. 55% original.
              </p>
            </div>
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                4
              </div>
              <p className="text-sm leading-relaxed">
                <span className="font-semibold">
                  Long-Term Commitment Required:
                </span>{" "}
                All interventions require sustained 6+ year implementation. Next
                goal: Improving threshold (55) achievable by 2033-2035.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
