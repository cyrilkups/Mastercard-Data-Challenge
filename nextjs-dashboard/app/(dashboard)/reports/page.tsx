"use client";

import { useState } from "react";
import {
  FileText,
  Download,
  FileSpreadsheet,
  Database,
  Calendar,
  Filter,
} from "lucide-react";
import { generatePDF } from "@/utils/pdfGenerator";
import { generateCSV } from "@/utils/csvGenerator";
import { exportToJSON } from "@/utils/jsonExporter";

export default function ReportsPage() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [reportType, setReportType] = useState("comprehensive");
  const [dateRange, setDateRange] = useState("all-time");

  const handleDownloadPDF = async () => {
    setIsGenerating(true);
    try {
      await generatePDF(reportType, dateRange);
    } catch (error) {
      console.error("Error generating PDF:", error);
      alert("Failed to generate PDF. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadCSV = async () => {
    setIsGenerating(true);
    try {
      await generateCSV(reportType, dateRange);
    } catch (error) {
      console.error("Error generating CSV:", error);
      alert("Failed to generate CSV. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportData = async () => {
    setIsGenerating(true);
    try {
      await exportToJSON(reportType, dateRange);
    } catch (error) {
      console.error("Error exporting data:", error);
      alert("Failed to export data. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-poppins font-bold text-gray-900">
          Reports & Analytics
        </h1>
        <p className="text-gray-600 mt-2">
          Generate and export comprehensive IGS reports in multiple formats
        </p>
      </div>

      {/* Report Configuration */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-xl font-poppins font-semibold text-gray-900 mb-6">
          Report Configuration
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Report Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Filter className="inline w-4 h-4 mr-2" />
              Report Type
            </label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent transition-all"
            >
              <option value="comprehensive">Comprehensive Report</option>
              <option value="summary">Executive Summary</option>
              <option value="trends">Trends Analysis</option>
              <option value="pillars">Pillar Breakdown</option>
              <option value="predictions">ML Predictions</option>
            </select>
          </div>

          {/* Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="inline w-4 h-4 mr-2" />
              Date Range
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-primary focus:border-transparent transition-all"
            >
              <option value="last-year">Last Year (2024)</option>
              <option value="all-time">All Time (2019-2024)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Export Options */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* PDF Export */}
        <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl p-6 border border-red-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-red-500 rounded-lg">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">PDF Report</h3>
              <p className="text-xs text-gray-600">
                Professional formatted document
              </p>
            </div>
          </div>
          <button
            onClick={handleDownloadPDF}
            disabled={isGenerating}
            className="w-full bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <Download className="w-4 h-4" />
            {isGenerating ? "Generating..." : "Download PDF"}
          </button>
        </div>

        {/* CSV Export */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-green-500 rounded-lg">
              <FileSpreadsheet className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">CSV Export</h3>
              <p className="text-xs text-gray-600">Raw data for analysis</p>
            </div>
          </div>
          <button
            onClick={handleDownloadCSV}
            disabled={isGenerating}
            className="w-full bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <Download className="w-4 h-4" />
            {isGenerating ? "Generating..." : "Download CSV"}
          </button>
        </div>

        {/* JSON Export */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-blue-500 rounded-lg">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">JSON Data</h3>
              <p className="text-xs text-gray-600">Structured data export</p>
            </div>
          </div>
          <button
            onClick={handleExportData}
            disabled={isGenerating}
            className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <Download className="w-4 h-4" />
            {isGenerating ? "Exporting..." : "Export Data"}
          </button>
        </div>
      </div>

      {/* Report Preview */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-xl font-poppins font-semibold text-gray-900 mb-6">
          Report Preview
        </h2>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="text-sm text-gray-600">Report Type</p>
              <p className="font-semibold text-gray-900 capitalize">
                {reportType.replace("-", " ")}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Date Range</p>
              <p className="font-semibold text-gray-900 capitalize">
                {dateRange.replace("-", " ")}
              </p>
            </div>
          </div>

          <div className="border-l-4 border-purple-primary pl-4 py-2 bg-purple-50">
            <p className="text-sm text-gray-700">
              <strong>Note:</strong> Reports include IGS scores, pillar
              breakdowns, trend analysis, and ML predictions based on your
              selected configuration.
            </p>
          </div>
        </div>
      </div>

      {/* Recent Reports */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-xl font-poppins font-semibold text-gray-900 mb-6">
          Recent Reports
        </h2>

        <div className="space-y-3">
          {[
            {
              name: "Comprehensive Report - Q4 2024",
              date: "Nov 28, 2024",
              type: "PDF",
              size: "2.4 MB",
            },
            {
              name: "Trends Analysis - 2024",
              date: "Nov 25, 2024",
              type: "CSV",
              size: "156 KB",
            },
            {
              name: "Pillar Breakdown - October",
              date: "Nov 20, 2024",
              type: "JSON",
              size: "89 KB",
            },
          ].map((report, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="p-2 bg-gray-100 rounded">
                  <FileText className="w-5 h-5 text-gray-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">{report.name}</p>
                  <p className="text-xs text-gray-500">
                    {report.date} • {report.type} • {report.size}
                  </p>
                </div>
              </div>
              <button className="text-purple-primary hover:text-purple-600 font-medium text-sm">
                Download
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
