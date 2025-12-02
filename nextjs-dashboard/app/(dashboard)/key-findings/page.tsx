"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface ChartSection {
  title: string;
  description: string;
  charts: {
    src: string;
    alt: string;
    caption: string;
  }[];
}

// Chart data
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

const placeRadarData = [
  { indicator: "Broadband", value2019: 44, value2024: 59 },
  { indicator: "Housing", value2019: 9, value2024: 14 },
  { indicator: "Infrastructure", value2019: 45, value2024: 32 },
  { indicator: "Environment", value2019: 38, value2024: 25 },
];

const incomeData = [
  { year: 2019, percentile: 36.9 },
  { year: 2020, percentile: 14.1 },
  { year: 2021, percentile: -2.9 },
  { year: 2022, percentile: -12.1 },
  { year: 2023, percentile: -15.6 },
  { year: 2024, percentile: -15.6 },
];

const businessData = [
  { year: 2019, growth: -40.0 },
  { year: 2020, growth: -35.2 },
  { year: 2021, growth: -30.5 },
  { year: 2022, growth: -25.8 },
  { year: 2023, growth: -20.0 },
  { year: 2024, growth: 8.3 },
];

const povertyData = [
  { year: 2019, overall: 22.0, child: 27.0, workingAge: 22.0, senior: 18.0 },
  { year: 2020, overall: 23.0, child: 28.0, workingAge: 23.0, senior: 19.0 },
  { year: 2021, overall: 24.0, child: 29.0, workingAge: 24.0, senior: 19.5 },
  { year: 2022, overall: 24.5, child: 29.5, workingAge: 24.5, senior: 19.8 },
  { year: 2023, overall: 25.0, child: 30.0, workingAge: 25.0, senior: 20.0 },
  { year: 2024, overall: 25.0, child: 30.0, workingAge: 25.0, senior: 20.0 },
];

const educationData = [
  { year: 2019, tract: 50.0, ruralAvg: 44.2 },
  { year: 2020, tract: 47.0, ruralAvg: 43.8 },
  { year: 2021, tract: 43.5, ruralAvg: 43.5 },
  { year: 2022, tract: 40.0, ruralAvg: 43.0 },
  { year: 2023, tract: 36.7, ruralAvg: 42.7 },
  { year: 2024, tract: 33.4, ruralAvg: 42.5 },
];

const communityRadarData = [
  { indicator: "Poverty", value2019: 78, value2024: 75 },
  { indicator: "Insurance", value2019: 77, value2024: 75 },
  { indicator: "Education", value2019: 50, value2024: 33 },
  { indicator: "Social Capital", value2019: 65, value2024: 55 },
];

const chartSections: ChartSection[] = [];

const criticalInsights = [
  {
    number: "1",
    title: "Compounding Vulnerabilities",
    text: "Economic decline (income -15.6%, business -33.3%) drives housing unaffordability (86.5% burden) and limits community investments, creating a self-reinforcing downward spiral.",
  },
  {
    number: "2",
    title: "Infrastructure Deficits",
    text: "Severe broadband gap (28.6pp below U.S.) limits remote work, economic development, educational access, and telehealth services.",
  },
  {
    number: "3",
    title: "Affordability Crisis",
    text: "86.5% housing cost burden severely limits savings, healthcare spending, educational investments, and economic mobility.",
  },
  {
    number: "4",
    title: "Business Ecosystem Collapse",
    text: "-33.3% net business growth indicates entrepreneurial flight and self-reinforcing decline cycle.",
  },
  {
    number: "5",
    title: "Human Capital Challenges",
    text: "High poverty + low insurance + limited early education creates barriers to workforce development and intergenerational mobility.",
  },
  {
    number: "6",
    title: "Declining Trends",
    text: "Multiple indicators show deterioration (2019-2024): Income -52.5pp, Place -13pts, Community -14pts, Early Ed -16.6pp, IGS 40→27.",
  },
];

type ChartType =
  | "broadband"
  | "housing"
  | "place-radar"
  | "income"
  | "business"
  | "poverty"
  | "education"
  | "community-radar"
  | null;

export default function KeyFindingsPage() {
  const [selectedChart, setSelectedChart] = useState<ChartType>(null);

  const renderExpandedChart = () => {
    if (!selectedChart) return null;

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
              <linearGradient
                id="colorBurdenExpanded"
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
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[0, 100]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="burden"
              stroke="#ef4444"
              fill="url(#colorBurdenExpanded)"
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
      "place-radar": {
        title: "Place Score Components Comparison",
        component: (
          <RadarChart data={placeRadarData}>
            <PolarGrid stroke="#e5e7eb" />
            <PolarAngleAxis dataKey="indicator" stroke="#6b7280" />
            <PolarRadiusAxis domain={[0, 100]} stroke="#6b7280" />
            <Radar
              name="2019"
              dataKey="value2019"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.3}
              strokeWidth={2}
            />
            <Radar
              name="2024"
              dataKey="value2024"
              stroke="#ef4444"
              fill="#ef4444"
              fillOpacity={0.3}
              strokeWidth={2}
            />
            <Legend />
          </RadarChart>
        ),
      },
      income: {
        title: "Median Income Percentile Trends",
        component: (
          <AreaChart data={incomeData}>
            <defs>
              <linearGradient
                id="colorIncomeExpanded"
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
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[-20, 40]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Area
              type="monotone"
              dataKey="percentile"
              stroke="#ef4444"
              fill="url(#colorIncomeExpanded)"
              name="Income Percentile"
              strokeWidth={2}
            />
          </AreaChart>
        ),
      },
      business: {
        title: "Business Growth Trends",
        component: (
          <BarChart data={businessData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis domain={[-45, 15]} stroke="#6b7280" />
            <Tooltip />
            <Legend />
            <Bar dataKey="growth" fill="#ef4444" name="Net Business Growth %" />
          </BarChart>
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
              name="Overall"
            />
            <Line
              type="monotone"
              dataKey="child"
              stroke="#dc2626"
              strokeWidth={3}
              name="Child (<18)"
            />
            <Line
              type="monotone"
              dataKey="workingAge"
              stroke="#f97316"
              strokeWidth={3}
              name="Working Age"
            />
            <Line
              type="monotone"
              dataKey="senior"
              stroke="#fb923c"
              strokeWidth={3}
              name="Senior (65+)"
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
      "community-radar": {
        title: "Community Score Components Comparison",
        component: (
          <RadarChart data={communityRadarData}>
            <PolarGrid stroke="#e5e7eb" />
            <PolarAngleAxis dataKey="indicator" stroke="#6b7280" />
            <PolarRadiusAxis domain={[0, 100]} stroke="#6b7280" />
            <Radar
              name="2019"
              dataKey="value2019"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.3}
              strokeWidth={2}
            />
            <Radar
              name="2024"
              dataKey="value2024"
              stroke="#ef4444"
              fill="#ef4444"
              fillOpacity={0.3}
              strokeWidth={2}
            />
            <Legend />
          </RadarChart>
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
          <div className="p-6 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">{config.title}</h2>
            <button
              onClick={() => setSelectedChart(null)}
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-8">
      {renderExpandedChart()}
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Key Findings: Comprehensive Analysis
          </h1>
          <p className="text-lg text-gray-600">
            Tract 20800 Analysis (2019-2024) • Bottom 20-40th Percentile
            Performance
          </p>
        </div>

        {/* Executive Summary */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8 border-l-4 border-red-500">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">
            Executive Summary
          </h2>
          <p className="text-gray-700 leading-relaxed">
            Tract 20800 exhibits{" "}
            <span className="font-semibold text-red-600">
              severe, compounding distress
            </span>{" "}
            across all three pillars of inclusive growth. The tract ranks in the{" "}
            <span className="font-semibold">
              bottom 20-40th percentile nationally
            </span>{" "}
            across most indicators, with particularly acute challenges in
            broadband access, housing affordability, and economic vitality.
            Trends from 2019-2024 show{" "}
            <span className="font-semibold text-red-600">
              declining or stagnant conditions
            </span>
            , indicating systemic challenges requiring comprehensive,
            multi-sector intervention.
          </p>
        </div>

        {/* Place Pillar Charts */}
        <div className="mb-12">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Place Pillar Analysis
            </h2>
            <p className="text-gray-600">
              Infrastructure and environmental quality indicators showing severe
              deficits in broadband access and housing affordability.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {/* Broadband Trends */}
            <div
              onClick={() => setSelectedChart("broadband")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Broadband Access Trends
              </h3>
              <ResponsiveContainer width="100%" height={280}>
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
                    strokeWidth={2}
                    name="Tract 20800"
                  />
                  <Line
                    type="monotone"
                    dataKey="arkansas"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    name="Arkansas"
                  />
                  <Line
                    type="monotone"
                    dataKey="usa"
                    stroke="#22c55e"
                    strokeWidth={2}
                    name="USA"
                  />
                </LineChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Broadband access improved from 44.1% (2019) to 58.7% (2024), but
                remains 28.6 percentage points below U.S. average
              </p>
            </div>

            {/* Housing Burden */}
            <div
              onClick={() => setSelectedChart("housing")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Housing Cost Burden
              </h3>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={housingData}>
                  <defs>
                    <linearGradient
                      id="colorBurden"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                      <stop
                        offset="95%"
                        stopColor="#ef4444"
                        stopOpacity={0.2}
                      />
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
                    fill="url(#colorBurden)"
                    name="Cost Burdened %"
                  />
                  <Line
                    type="monotone"
                    dataKey="threshold"
                    stroke="#22c55e"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    name="Affordable Threshold"
                  />
                </AreaChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Extreme housing crisis: 86.5% of households cost-burdened, far
                exceeding 30% affordability threshold
              </p>
            </div>

            {/* Place Radar */}
            <div
              onClick={() => setSelectedChart("place-radar")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Place Score Components
              </h3>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={placeRadarData}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis dataKey="indicator" stroke="#6b7280" />
                  <PolarRadiusAxis domain={[0, 100]} stroke="#6b7280" />
                  <Radar
                    name="2019"
                    dataKey="value2019"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="2024"
                    dataKey="value2024"
                    stroke="#ef4444"
                    fill="#ef4444"
                    fillOpacity={0.3}
                  />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Place score declined from 34 (2019) to 21 (2024), indicating
                deteriorating infrastructure quality
              </p>
            </div>
          </div>
        </div>

        {/* Economy Pillar Charts */}
        <div className="mb-12">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Economy Pillar Analysis
            </h2>
            <p className="text-gray-600">
              Economic vitality indicators revealing severe income decline and
              business ecosystem collapse.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Income Trends */}
            <div
              onClick={() => setSelectedChart("income")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Median Income Percentile Trends
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={incomeData}>
                  <defs>
                    <linearGradient
                      id="colorIncome"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                      <stop
                        offset="95%"
                        stopColor="#ef4444"
                        stopOpacity={0.2}
                      />
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
                    fill="url(#colorIncome)"
                    name="Income Percentile"
                  />
                </AreaChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Median income fell 52.5 percentile points (36.9 to -15.6)
                indicating severe economic decline
              </p>
            </div>

            {/* Business Growth */}
            <div
              onClick={() => setSelectedChart("business")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Business Growth Trends
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={businessData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="year" stroke="#6b7280" />
                  <YAxis domain={[-45, 15]} stroke="#6b7280" />
                  <Tooltip />
                  <Legend />
                  <Bar
                    dataKey="growth"
                    fill="#ef4444"
                    name="Net Business Growth %"
                  />
                </BarChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Business growth shows ecosystem stress with recent recovery to
                8.3% in 2024
              </p>
            </div>
          </div>
        </div>

        {/* Community Pillar Charts */}
        <div className="mb-12">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Community Pillar Analysis
            </h2>
            <p className="text-gray-600">
              Social capital and human development indicators showing challenges
              in poverty, education, and health access.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {/* Poverty Trends */}
            <div
              onClick={() => setSelectedChart("poverty")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Poverty Rates by Age Group
              </h3>
              <ResponsiveContainer width="100%" height={280}>
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
                    strokeWidth={2}
                    name="Overall"
                  />
                  <Line
                    type="monotone"
                    dataKey="child"
                    stroke="#dc2626"
                    strokeWidth={2}
                    name="Child (<18)"
                  />
                  <Line
                    type="monotone"
                    dataKey="workingAge"
                    stroke="#f97316"
                    strokeWidth={2}
                    name="Working Age"
                  />
                  <Line
                    type="monotone"
                    dataKey="senior"
                    stroke="#fb923c"
                    strokeWidth={2}
                    name="Senior (65+)"
                  />
                </LineChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Overall poverty ~25%, child poverty ~30%, significantly above
                15.4% rural average
              </p>
            </div>

            {/* Early Education */}
            <div
              onClick={() => setSelectedChart("education")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Early Education Enrollment
              </h3>
              <ResponsiveContainer width="100%" height={280}>
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
                    strokeWidth={2}
                    name="Tract 20800"
                  />
                  <Line
                    type="monotone"
                    dataKey="ruralAvg"
                    stroke="#22c55e"
                    strokeWidth={2}
                    name="Rural Average"
                  />
                </LineChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Early education enrollment declined from 50% (2019) to 33.4%
                (2024), 9.1 points below rural average
              </p>
            </div>

            {/* Community Radar */}
            <div
              onClick={() => setSelectedChart("community-radar")}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-all duration-200 cursor-pointer hover:scale-[1.02]"
            >
              <h3 className="font-semibold text-gray-900 mb-4">
                Community Score Components
              </h3>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={communityRadarData}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis dataKey="indicator" stroke="#6b7280" />
                  <PolarRadiusAxis domain={[0, 100]} stroke="#6b7280" />
                  <Radar
                    name="2019"
                    dataKey="value2019"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="2024"
                    dataKey="value2024"
                    stroke="#ef4444"
                    fill="#ef4444"
                    fillOpacity={0.3}
                  />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
              <p className="text-sm text-gray-700 mt-4">
                Community score fell from 54 (2019) to 40 (2024), indicating
                declining social capital
              </p>
            </div>
          </div>
        </div>

        {/* Critical Cross-Cutting Insights */}
        <div className="mt-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Critical Cross-Cutting Insights
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {criticalInsights.map((insight, idx) => (
              <div
                key={idx}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-lg">
                    {insight.number}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {insight.title}
                    </h3>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      {insight.text}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Conclusion */}
        <div className="mt-12 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">
            Conclusion & Recommendation
          </h2>
          <p className="leading-relaxed mb-4">
            Tract 20800 faces severe, systemic challenges across all three
            pillars. The tract exhibits
            <span className="font-semibold">
              {" "}
              BOTTOM 20-40TH PERCENTILE
            </span>{" "}
            performance nationally with
            <span className="font-semibold"> DECLINING TRENDS</span> and{" "}
            <span className="font-semibold">COMPOUNDING VULNERABILITIES</span>.
          </p>
          <p className="leading-relaxed">
            Without comprehensive intervention, continued decline is projected.
            However, targeted interventions addressing broadband infrastructure,
            housing affordability, business support, and human capital
            development show potential to reverse these trends.
          </p>
          <div className="mt-6 p-4 bg-white/10 rounded-lg">
            <p className="font-semibold text-lg">
              Recommended: COMPREHENSIVE, MULTI-SECTOR INTERVENTION STRATEGY
            </p>
            <p className="text-sm mt-2">
              Focus on breaking the cycle of compounding vulnerabilities and
              building foundational assets across place, economy, and community
              pillars.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
