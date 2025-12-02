"use client";

import { useEffect, useState } from "react";
import {
  Save,
  Check,
  User,
  Bell,
  Database,
  FileText,
  Shield,
  Globe,
} from "lucide-react";

type Settings = {
  theme: "light" | "dark";
  refreshInterval: number;
  dataSource: "sample" | "file";
  defaultExportFormat: "pdf" | "csv" | "json";
  notifications: {
    email: boolean;
    push: boolean;
    reports: boolean;
    alerts: boolean;
  };
  user: {
    name: string;
    email: string;
    role: string;
  };
  display: {
    compactMode: boolean;
    showTrends: boolean;
    animationsEnabled: boolean;
  };
};

const DEFAULTS: Settings = {
  theme: "light",
  refreshInterval: 5,
  dataSource: "file",
  defaultExportFormat: "pdf",
  notifications: {
    email: true,
    push: true,
    reports: true,
    alerts: true,
  },
  user: {
    name: "Cyril Kups",
    email: "cyril@datanova.com",
    role: "Administrator",
  },
  display: {
    compactMode: false,
    showTrends: true,
    animationsEnabled: true,
  },
};

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>(DEFAULTS);
  const [saved, setSaved] = useState(false);
  const [activeTab, setActiveTab] = useState<
    "general" | "notifications" | "display" | "account"
  >("general");

  useEffect(() => {
    const raw = localStorage.getItem("datanova_settings");
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        setSettings({ ...DEFAULTS, ...parsed });
      } catch {}
    }
  }, []);

  const save = () => {
    localStorage.setItem("datanova_settings", JSON.stringify(settings));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const resetToDefaults = () => {
    if (confirm("Are you sure you want to reset all settings to defaults?")) {
      setSettings(DEFAULTS);
      localStorage.setItem("datanova_settings", JSON.stringify(DEFAULTS));
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    }
  };

  const tabs = [
    { id: "general", label: "General", icon: Globe },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "display", label: "Display", icon: FileText },
    { id: "account", label: "Account", icon: User },
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-poppins font-bold text-gray-900">
            Settings
          </h1>
          <p className="text-gray-600 mt-2">
            Configure your dashboard preferences and account settings
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={resetToDefaults}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Reset to Defaults
          </button>
          <button
            onClick={save}
            className="px-6 py-2 bg-gradient-to-r from-purple-primary to-purple-600 text-white rounded-lg hover:shadow-lg transition-all flex items-center gap-2"
          >
            {saved ? <Check size={18} /> : <Save size={18} />}
            {saved ? "Saved!" : "Save Changes"}
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="border-b border-gray-200">
          <div className="flex">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-6 py-4 font-medium transition-all ${
                    activeTab === tab.id
                      ? "text-purple-primary border-b-2 border-purple-primary"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  <Icon size={18} />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-8">
          {/* General Tab */}
          {activeTab === "general" && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Theme
                </label>
                <div className="flex gap-4">
                  <label className="flex-1 cursor-pointer">
                    <input
                      type="radio"
                      name="theme"
                      checked={settings.theme === "light"}
                      onChange={() =>
                        setSettings({ ...settings, theme: "light" })
                      }
                      className="sr-only"
                    />
                    <div
                      className={`p-4 border-2 rounded-lg text-center transition-all ${
                        settings.theme === "light"
                          ? "border-purple-primary bg-purple-50"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <div className="text-2xl mb-2">☀️</div>
                      <div className="font-medium">Light</div>
                    </div>
                  </label>
                  <label className="flex-1 cursor-pointer">
                    <input
                      type="radio"
                      name="theme"
                      checked={settings.theme === "dark"}
                      onChange={() =>
                        setSettings({ ...settings, theme: "dark" })
                      }
                      className="sr-only"
                    />
                    <div
                      className={`p-4 border-2 rounded-lg text-center transition-all ${
                        settings.theme === "dark"
                          ? "border-purple-primary bg-purple-50"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <div className="text-2xl mb-2">🌙</div>
                      <div className="font-medium">Dark</div>
                    </div>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Data Source
                </label>
                <select
                  value={settings.dataSource}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      dataSource: e.target.value as Settings["dataSource"],
                    })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent"
                >
                  <option value="sample">Sample Data (Embedded)</option>
                  <option value="file">Live Data (File System)</option>
                </select>
                <p className="text-xs text-gray-500 mt-2">
                  Live Data reads from igs_ml/data/igs_trends_features.csv and
                  ML models
                </p>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Default Export Format
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {["pdf", "csv", "json"].map((format) => (
                    <label key={format} className="cursor-pointer">
                      <input
                        type="radio"
                        name="exportFormat"
                        checked={settings.defaultExportFormat === format}
                        onChange={() =>
                          setSettings({
                            ...settings,
                            defaultExportFormat: format as any,
                          })
                        }
                        className="sr-only"
                      />
                      <div
                        className={`p-3 border-2 rounded-lg text-center transition-all ${
                          settings.defaultExportFormat === format
                            ? "border-purple-primary bg-purple-50"
                            : "border-gray-200 hover:border-gray-300"
                        }`}
                      >
                        <div className="font-medium uppercase">{format}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Auto-Refresh Interval: {settings.refreshInterval}s
                </label>
                <input
                  type="range"
                  min={1}
                  max={60}
                  value={settings.refreshInterval}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      refreshInterval: Number(e.target.value),
                    })
                  }
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>1s</span>
                  <span>30s</span>
                  <span>60s</span>
                </div>
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === "notifications" && (
            <div className="space-y-4">
              {[
                {
                  key: "email",
                  label: "Email Notifications",
                  desc: "Receive updates via email",
                },
                {
                  key: "push",
                  label: "Push Notifications",
                  desc: "Browser push notifications",
                },
                {
                  key: "reports",
                  label: "Report Notifications",
                  desc: "Weekly and monthly reports",
                },
                {
                  key: "alerts",
                  label: "Alert Notifications",
                  desc: "Critical alerts and warnings",
                },
              ].map((item) => (
                <div
                  key={item.key}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div>
                    <div className="font-medium text-gray-900">
                      {item.label}
                    </div>
                    <div className="text-sm text-gray-500">{item.desc}</div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={
                        settings.notifications[
                          item.key as keyof typeof settings.notifications
                        ]
                      }
                      onChange={(e) =>
                        setSettings({
                          ...settings,
                          notifications: {
                            ...settings.notifications,
                            [item.key]: e.target.checked,
                          },
                        })
                      }
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-primary"></div>
                  </label>
                </div>
              ))}
            </div>
          )}

          {/* Display Tab */}
          {activeTab === "display" && (
            <div className="space-y-4">
              {[
                {
                  key: "compactMode",
                  label: "Compact Mode",
                  desc: "Reduce spacing and padding",
                },
                {
                  key: "showTrends",
                  label: "Show Trend Indicators",
                  desc: "Display up/down arrows on metrics",
                },
                {
                  key: "animationsEnabled",
                  label: "Enable Animations",
                  desc: "Smooth transitions and effects",
                },
              ].map((item) => (
                <div
                  key={item.key}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div>
                    <div className="font-medium text-gray-900">
                      {item.label}
                    </div>
                    <div className="text-sm text-gray-500">{item.desc}</div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={
                        settings.display[
                          item.key as keyof typeof settings.display
                        ]
                      }
                      onChange={(e) =>
                        setSettings({
                          ...settings,
                          display: {
                            ...settings.display,
                            [item.key]: e.target.checked,
                          },
                        })
                      }
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-primary"></div>
                  </label>
                </div>
              ))}
            </div>
          )}

          {/* Account Tab */}
          {activeTab === "account" && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={settings.user.name}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      user: { ...settings.user, name: e.target.value },
                    })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={settings.user.email}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      user: { ...settings.user, email: e.target.value },
                    })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Role
                </label>
                <select
                  value={settings.user.role}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      user: { ...settings.user, role: e.target.value },
                    })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent"
                >
                  <option value="Administrator">Administrator</option>
                  <option value="Analyst">Analyst</option>
                  <option value="Viewer">Viewer</option>
                </select>
              </div>
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-sm font-semibold text-gray-900 mb-4">
                  Danger Zone
                </h3>
                <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors">
                  Delete Account
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
