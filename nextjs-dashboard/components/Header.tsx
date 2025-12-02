"use client";

import { useState } from "react";
import Image from "next/image";
import { Search, Bell, ChevronDown } from "lucide-react";

export default function Header() {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  const notifications = [
    {
      id: 1,
      text: "New IGS data available for Q4 2024",
      time: "5 min ago",
      unread: true,
    },
    {
      id: 2,
      text: "ML prediction model updated successfully",
      time: "1 hour ago",
      unread: true,
    },
    {
      id: 3,
      text: "Weekly report generated",
      time: "2 hours ago",
      unread: false,
    },
  ];

  const unreadCount = notifications.filter((n) => n.unread).length;

  return (
    <header className="bg-white border-b border-gray-200 px-8 py-4">
      <div className="flex items-center justify-between">
        {/* Welcome Text */}
        <div>
          <h2 className="text-2xl font-poppins font-semibold text-gray-900">
            Welcome back, Cyril
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Here&apos;s what&apos;s happening with your analytics today
          </p>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-6">
          {/* Search */}
          <button
            onClick={() => setShowSearch(true)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Search size={20} className="text-gray-600" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors relative"
            >
              <Bell size={20} className="text-gray-600" />
              {unreadCount > 0 && (
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <h3 className="font-semibold text-gray-900">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map((notif) => (
                    <div
                      key={notif.id}
                      className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                        notif.unread ? "bg-blue-50/30" : ""
                      }`}
                    >
                      <p className="text-sm text-gray-900">{notif.text}</p>
                      <p className="text-xs text-gray-500 mt-1">{notif.time}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Profile */}
          <div className="relative">
            <button
              onClick={() => setShowProfile(!showProfile)}
              className="flex items-center gap-3 hover:bg-gray-100 px-3 py-2 rounded-lg transition-colors"
            >
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-primary to-orange-accent flex items-center justify-center text-white font-semibold text-sm">
                CK
              </div>
              <ChevronDown size={16} className="text-gray-600" />
            </button>

            {/* Profile Dropdown */}
            {showProfile && (
              <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <p className="font-semibold text-gray-900">Cyril Kups</p>
                  <p className="text-sm text-gray-500">cyril@igsplatform.com</p>
                </div>
                <div className="p-2">
                  <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
                    Profile Settings
                  </button>
                  <button className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg mt-2">
                    Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Search Modal */}
      {showSearch && (
        <div
          className="fixed inset-0 bg-black/50 flex items-start justify-center z-50 pt-20"
          onClick={() => setShowSearch(false)}
        >
          <div
            className="bg-white rounded-xl p-6 max-w-2xl w-full mx-4 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center gap-3 mb-4">
              <Search size={20} className="text-gray-400" />
              <input
                type="text"
                placeholder="Search for pages, features, reports..."
                autoFocus
                className="flex-1 text-lg outline-none"
              />
            </div>
            <div className="space-y-2">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
                Quick Links
              </p>
              <button className="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg text-sm">
                📊 Overview Dashboard
              </button>
              <button className="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg text-sm">
                🎮 Policy Simulation
              </button>
              <button className="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg text-sm">
                📄 Export Reports
              </button>
              <button className="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-lg text-sm">
                ⚙️ Settings
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
