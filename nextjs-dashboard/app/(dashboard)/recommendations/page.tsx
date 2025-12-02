"use client";

import {
  CheckCircle2,
  TrendingUp,
  Users,
  Home,
  Briefcase,
  Target,
  ArrowRight,
  Lightbulb,
} from "lucide-react";

export default function RecommendationsPage() {
  const recommendations = [
    {
      id: 1,
      category: "Housing & Infrastructure",
      icon: Home,
      priority: "High",
      priorityColor: "red",
      title: "Reduce Housing Cost Burden",
      description:
        "Current housing cost burden of 86.5% is critically high. Target reduction to 78% can yield significant IGS improvements across all pillars.",
      impact: "High Impact",
      timeframe: "12-18 months",
      actions: [
        "Reduce housing cost burden from 86.5% to 78% (-8.5 percentage points)",
        "Implement affordable housing development programs",
        "Provide rental assistance and housing vouchers for low-income families",
        "Partner with developers for mixed-income housing projects",
      ],
      metrics: {
        current: 21.0,
        target: 37.6,
        improvement: "+79%",
        igsGain: 10.3,
      },
      details: {
        placeGain: 16.6,
        economyGain: 10.4,
        communityGain: 6.2,
      },
    },
    {
      id: 2,
      category: "Community Development",
      icon: Users,
      priority: "High",
      priorityColor: "red",
      title: "Expand Early Education Enrollment",
      description:
        "Increasing early education enrollment from 33.4% to 37.5% shows strongest Place pillar impact (+18.9 points) and high IGS gains.",
      impact: "High Impact",
      timeframe: "9-15 months",
      actions: [
        "Increase early education enrollment from 33.4% to 37.5% (+4.1 percentage points)",
        "Expand Head Start and universal pre-K programs",
        "Provide childcare subsidies for working families",
        "Build new early learning centers in underserved areas",
      ],
      metrics: {
        current: 21.0,
        target: 39.9,
        improvement: "+90%",
        igsGain: 10.3,
      },
      details: {
        placeGain: 18.9,
        economyGain: 10.6,
        communityGain: 6.4,
      },
    },
    {
      id: 3,
      category: "Economic Development",
      icon: Briefcase,
      priority: "High",
      priorityColor: "red",
      title: "Strengthen Small Business Support",
      description:
        "Boosting minority-owned businesses from 8.3% to 9.5% achieves highest IGS gain (+10.5 points) with strongest economy pillar impact.",
      impact: "High Impact",
      timeframe: "6-12 months",
      actions: [
        "Increase minority-owned businesses from 8.3% to 9.5% (+1.2 percentage points)",
        "Establish microloans and technical assistance programs",
        "Create entrepreneur mentorship connecting business owners with experts",
        "Implement procurement preferences for minority-owned businesses",
      ],
      metrics: {
        current: 20.0,
        target: 30.8,
        improvement: "+54%",
        igsGain: 10.5,
      },
      details: {
        placeGain: 16.5,
        economyGain: 10.8,
        communityGain: 1.7,
      },
    },
    {
      id: 4,
      category: "Integrated Strategy",
      icon: Target,
      priority: "Critical",
      priorityColor: "red",
      title: "Combined Intervention Approach",
      description:
        "Implementing all three interventions simultaneously achieves maximum impact: IGS 27.0 → 37.5 (+10.5 points, 39% improvement).",
      impact: "Maximum Impact",
      timeframe: "12-18 months",
      actions: [
        "Deploy housing affordability, early education, and business support programs concurrently",
        "Leverage synergies: affordable housing enables education access",
        "Education quality attracts businesses and strengthens workforce",
        "Track integrated KPIs across all three intervention areas",
      ],
      metrics: {
        current: 27.0,
        target: 37.5,
        improvement: "+39%",
        igsGain: 10.5,
      },
      details: {
        placeGain: 18.9,
        economyGain: 10.9,
        communityGain: 1.7,
      },
    },
  ];

  const getPriorityBadge = (priority: string, color: string) => {
    const colors = {
      red: "bg-red-100 text-red-700 border-red-200",
      yellow: "bg-yellow-100 text-yellow-700 border-yellow-200",
      green: "bg-green-100 text-green-700 border-green-200",
    };
    return colors[color as keyof typeof colors] || colors.yellow;
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="bg-gradient-to-r from-purple-primary to-purple-600 rounded-2xl p-8 text-white">
        <div className="flex items-center gap-3 mb-4">
          <Lightbulb className="w-10 h-10" />
          <h1 className="text-4xl font-poppins font-bold">
            Strategic Recommendations
          </h1>
        </div>
        <p className="text-purple-100 text-lg max-w-3xl">
          Data-driven policy recommendations to improve IGS performance across
          all three pillars. Prioritized by impact potential and implementation
          feasibility.
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <Target className="w-5 h-5 text-red-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Critical Priority</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">4</p>
          <p className="text-sm text-gray-600 mt-1">
            All interventions high-impact
          </p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Projected Impact</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">+10.5</p>
          <p className="text-sm text-gray-600 mt-1">
            IGS points (39% improvement)
          </p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Model Accuracy</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">R²=0.73</p>
          <p className="text-sm text-gray-600 mt-1">Random Forest prediction</p>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="space-y-6">
        {recommendations.map((rec, index) => {
          const Icon = rec.icon;
          return (
            <div
              key={rec.id}
              className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover-lift"
            >
              {/* Header */}
              <div className="bg-gradient-to-r from-gray-50 to-white p-6 border-b border-gray-200">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-purple-100 rounded-xl">
                      <Icon className="w-7 h-7 text-purple-primary" />
                    </div>
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <h2 className="text-2xl font-poppins font-bold text-gray-900">
                          {rec.title}
                        </h2>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold border ${getPriorityBadge(
                            rec.priority,
                            rec.priorityColor
                          )}`}
                        >
                          {rec.priority} Priority
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 uppercase tracking-wide">
                        {rec.category}
                      </p>
                    </div>
                  </div>
                </div>

                <p className="text-gray-700 leading-relaxed">
                  {rec.description}
                </p>
              </div>

              {/* Content */}
              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Action Items */}
                  <div className="lg:col-span-2">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-purple-primary" />
                      Recommended Actions
                    </h3>
                    <ul className="space-y-3">
                      {rec.actions.map((action, idx) => (
                        <li key={idx} className="flex items-start gap-3 group">
                          <div className="mt-1 flex-shrink-0">
                            <ArrowRight className="w-4 h-4 text-purple-primary group-hover:translate-x-1 transition-transform" />
                          </div>
                          <span className="text-gray-700">{action}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Metrics */}
                  <div className="space-y-4">
                    <div className="bg-purple-50 rounded-xl p-5 border border-purple-200">
                      <h4 className="text-sm font-semibold text-purple-900 mb-4">
                        Expected Outcomes
                      </h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs text-purple-700 mb-1">
                            Current Place Score
                          </p>
                          <p className="text-2xl font-bold text-purple-900">
                            {rec.metrics.current}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-purple-700 mb-1">
                            Target Place Score
                          </p>
                          <p className="text-2xl font-bold text-purple-900">
                            {rec.metrics.target.toFixed(1)}
                          </p>
                        </div>
                        <div className="pt-3 border-t border-purple-200">
                          <p className="text-xs text-purple-700 mb-1">
                            Place Improvement
                          </p>
                          <p className="text-xl font-bold text-green-600 flex items-center gap-1">
                            <TrendingUp size={18} />
                            {rec.metrics.improvement}
                          </p>
                        </div>
                        <div className="pt-3 border-t border-purple-200">
                          <p className="text-xs text-purple-700 mb-1">
                            IGS Score Gain
                          </p>
                          <p className="text-2xl font-bold text-green-600">
                            +{rec.metrics.igsGain.toFixed(1)}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                      <h4 className="text-xs font-semibold text-gray-700 mb-3">
                        Pillar Impacts
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Place:</span>
                          <span className="font-semibold text-green-600">
                            +{rec.details.placeGain.toFixed(1)}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Economy:</span>
                          <span className="font-semibold text-green-600">
                            +{rec.details.economyGain.toFixed(1)}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Community:</span>
                          <span className="font-semibold text-green-600">
                            +{rec.details.communityGain.toFixed(1)}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 gap-3">
                      <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                        <p className="text-xs text-gray-600 mb-1">Impact</p>
                        <p className="text-sm font-semibold text-gray-900">
                          {rec.impact}
                        </p>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                        <p className="text-xs text-gray-600 mb-1">Timeframe</p>
                        <p className="text-sm font-semibold text-gray-900">
                          {rec.timeframe}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Implementation Roadmap */}
      <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
        <h2 className="text-2xl font-poppins font-bold text-gray-900 mb-6">
          Implementation Roadmap
        </h2>
        <div className="space-y-4">
          <div className="flex items-start gap-4 p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
            <div className="flex-shrink-0 w-16 text-center">
              <p className="text-xs text-red-700 font-semibold">Q1 2025</p>
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">
                Phase 1: Launch All Three Interventions
              </p>
              <p className="text-sm text-gray-700 mt-1">
                Begin housing affordability (reduce burden 86.5% → 78%), early
                education expansion (33.4% → 37.5%), and minority business
                support (8.3% → 9.5%)
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
            <div className="flex-shrink-0 w-16 text-center">
              <p className="text-xs text-yellow-700 font-semibold">
                Q2-Q3 2025
              </p>
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">
                Phase 2: Monitor & Adjust
              </p>
              <p className="text-sm text-gray-700 mt-1">
                Track quarterly KPIs, measure early outcomes, refine programs
                based on data feedback
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
            <div className="flex-shrink-0 w-16 text-center">
              <p className="text-xs text-green-700 font-semibold">Q4 2025+</p>
            </div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">
                Phase 3: Achieve Targets
              </p>
              <p className="text-sm text-gray-700 mt-1">
                Expected IGS score: 37.5 (+10.5 points, 39% gain). Evaluate
                success, scale effective programs, plan next growth phase
              </p>
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-900">
            <strong>Data Source:</strong> Predictions based on Random Forest
            models (R²=0.73) trained on Lonoke County + 3 solution counties
            (Beltrami MN, Chaffee CO, Fulton GA). See AUGMENTED_MODEL_SUMMARY.md
            for full methodology.
          </p>
        </div>
      </div>
    </div>
  );
}
