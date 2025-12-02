"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { useState } from "react";
import {
  LayoutDashboard,
  TrendingUp,
  BarChart3,
  Brain,
  Sliders,
  FileText,
  FileSpreadsheet,
  Settings,
  HelpCircle,
  Mail,
  LogOut,
  X,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const navItems = [
  { name: "Overview", path: "/", icon: LayoutDashboard },
  { name: "IGS Trends", path: "/igs-trends", icon: TrendingUp },
  { name: "Indicators", path: "/indicators", icon: BarChart3 },
  { name: "ML Predictions", path: "/ml-predictions", icon: Brain },
  { name: "Policy Simulation", path: "/policy-simulation", icon: Sliders },
  { name: "Recommendations", path: "/recommendations", icon: FileText },
  { name: "Reports", path: "/reports", icon: FileSpreadsheet },
  { name: "Settings", path: "/settings", icon: Settings },
];

const supportItems = [
  { name: "Help Centre", icon: HelpCircle },
  { name: "Contact Us", icon: Mail },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [showHelp, setShowHelp] = useState(false);
  const [showContact, setShowContact] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleContactUs = () => {
    window.location.href =
      "mailto:cyrilkups95@gmail.com?subject=Data Nova Platform Support";
  };

  return (
    <>
      <aside
        className={`${
          isCollapsed ? "w-20" : "w-64"
        } bg-navy-deep text-white flex flex-col h-screen transition-all duration-300 relative`}
      >
        {/* Collapse Toggle Button */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute -right-3 top-8 bg-purple-primary hover:bg-purple-600 text-white rounded-full p-1.5 shadow-lg z-10 transition-colors"
        >
          {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>

        {/* Logo Section */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg overflow-hidden flex items-center justify-center flex-shrink-0">
              <Image
                src="/app-logo.png"
                alt="Data Nova Logo"
                width={40}
                height={40}
                className="object-contain"
              />
            </div>
            {!isCollapsed && (
              <div>
                <h1 className="text-xl font-poppins font-semibold">
                  Data Nova
                </h1>
                <p className="text-xs text-grey-muted">Analytics Dashboard</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 overflow-y-auto">
          <div className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.path;

              return (
                <Link
                  key={item.path}
                  href={item.path}
                  title={isCollapsed ? item.name : undefined}
                  className={`
                  flex items-center ${
                    isCollapsed ? "justify-center" : "gap-3"
                  } px-4 py-3 rounded-lg transition-all duration-200
                  ${
                    isActive
                      ? "bg-orange-accent text-white shadow-lg"
                      : "text-grey-muted hover:bg-white/5 hover:text-white"
                  }
                `}
                >
                  <Icon size={20} />
                  {!isCollapsed && (
                    <span className="text-sm font-medium">{item.name}</span>
                  )}
                </Link>
              );
            })}
          </div>

          {/* Help & Support Section */}
          <div className="mt-12 pt-6 border-t border-white/10">
            {!isCollapsed && (
              <p className="text-xs text-grey-muted uppercase tracking-wide mb-3 px-4">
                Help & Support
              </p>
            )}
            <div className="space-y-1">
              <button
                onClick={() => setShowHelp(true)}
                title={isCollapsed ? "Help Centre" : undefined}
                className={`w-full flex items-center ${
                  isCollapsed ? "justify-center" : "gap-3"
                } px-4 py-3 rounded-lg text-grey-muted hover:bg-white/5 hover:text-white transition-all duration-200`}
              >
                <HelpCircle size={20} />
                {!isCollapsed && (
                  <span className="text-sm font-medium">Help Centre</span>
                )}
              </button>
              <button
                onClick={handleContactUs}
                title={isCollapsed ? "Contact Us" : undefined}
                className={`w-full flex items-center ${
                  isCollapsed ? "justify-center" : "gap-3"
                } px-4 py-3 rounded-lg text-grey-muted hover:bg-white/5 hover:text-white transition-all duration-200`}
              >
                <Mail size={20} />
                {!isCollapsed && (
                  <span className="text-sm font-medium">Contact Us</span>
                )}
              </button>
            </div>
          </div>
        </nav>

        {/* Logout Button */}
        <div className="p-4 border-t border-white/10">
          <button
            title={isCollapsed ? "Logout" : undefined}
            className={`w-full flex items-center ${
              isCollapsed ? "justify-center" : "gap-3"
            } px-4 py-3 rounded-lg text-grey-muted hover:bg-red-500/10 hover:text-red-400 transition-all duration-200 group`}
          >
            <LogOut
              size={20}
              className="group-hover:scale-110 transition-transform"
            />
            {!isCollapsed && (
              <span className="text-sm font-medium">Logout</span>
            )}
          </button>
        </div>
      </aside>

      {/* Help Center Modal */}
      {showHelp && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          onClick={() => setShowHelp(false)}
        >
          <div
            className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-poppins font-bold text-gray-900">
                How to Use Data Nova
              </h2>
              <button
                onClick={() => setShowHelp(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X size={24} />
              </button>
            </div>

            <div className="space-y-6 text-gray-700">
              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  📊 Overview Dashboard
                </h3>
                <p className="text-sm">
                  View key metrics, IGS scores, and pillar breakdowns for Lonoke
                  County. Track performance across Place, Economy, and Community
                  dimensions.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  📈 IGS Trends
                </h3>
                <p className="text-sm">
                  Analyze historical trends from 2019-2024. See how Lonoke
                  County&apos;s Inclusive Growth Score has changed over time
                  with interactive charts.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  🎯 Indicators
                </h3>
                <p className="text-sm">
                  Deep dive into specific metrics like median income, broadband
                  access, housing cost burden, early education enrollment, and
                  minority-owned businesses.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  🤖 ML Predictions
                </h3>
                <p className="text-sm">
                  View machine learning forecasts to 2030 based on Random Forest
                  models (R²=0.73). Compare baseline scenarios with intervention
                  outcomes.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  🎮 Policy Simulation
                </h3>
                <p className="text-sm">
                  <strong>Interactive tool</strong> to test &quot;what-if&quot;
                  scenarios. Adjust housing affordability, early education, and
                  business support sliders to see predicted impacts on IGS
                  scores.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  💡 Recommendations
                </h3>
                <p className="text-sm">
                  Get data-backed policy recommendations based on successful
                  interventions from similar counties (Beltrami, Chaffee,
                  Fulton).
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  📄 Reports
                </h3>
                <p className="text-sm">
                  Export comprehensive reports in PDF, CSV, or JSON formats.
                  Choose from comprehensive, summary, trends, pillars, or
                  predictions report types.
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  ⚙️ Settings
                </h3>
                <p className="text-sm">
                  Customize your experience with theme preferences, data
                  sources, notification settings, and display options.
                </p>
              </section>

              <div className="mt-8 p-4 bg-purple-50 rounded-lg border border-purple-200">
                <p className="text-sm font-medium text-purple-900">
                  💡 <strong>Pro Tip:</strong> Start with the Policy Simulation
                  to explore different intervention scenarios, then download
                  detailed reports to share your findings.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
