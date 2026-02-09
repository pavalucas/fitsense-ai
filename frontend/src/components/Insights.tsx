import React from "react";
import type { InsightsResponse } from "../types";
import {
  TrendingUp,
  AlertTriangle,
  Link as LinkIcon,
  Info,
  Lightbulb,
} from "lucide-react";

interface InsightsProps {
  data: InsightsResponse;
}

const Insights: React.FC<InsightsProps> = ({ data }) => {
  const getIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case "trend":
        return <TrendingUp className="w-5 h-5 text-blue-500" />;
      case "anomaly":
        return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      case "correlation":
        return <LinkIcon className="w-5 h-5 text-purple-500" />;
      default:
        return <Info className="w-5 h-5 text-gray-500" />;
    }
  };

  const getSignificanceBadge = (significance: string) => {
    let colorClass = "bg-gray-100 text-gray-800";
    switch (significance.toLowerCase()) {
      case "high":
        colorClass = "bg-red-100 text-red-800 border-red-200";
        break;
      case "medium":
        colorClass = "bg-yellow-100 text-yellow-800 border-yellow-200";
        break;
      case "low":
        colorClass = "bg-green-100 text-green-800 border-green-200";
        break;
    }
    return (
      <span
        className={`text-xs font-medium px-2.5 py-0.5 rounded border ${colorClass}`}
      >
        {significance} Impact
      </span>
    );
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Summary Card */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-100 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="p-2 bg-white rounded-lg shadow-sm">
            <Lightbulb className="w-6 h-6 text-indigo-600" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-indigo-900 mb-1">
              Analysis Summary
            </h2>
            <p className="text-indigo-800 leading-relaxed text-sm md:text-base opacity-90">
              {data.summary}
            </p>
          </div>
        </div>
      </div>

      {/* Insights Grid */}
      <div className="grid gap-4 md:grid-cols-2">
        {data.insights.map((insight, index) => (
          <div
            key={index}
            className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col"
          >
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-2">
                {getIcon(insight.type)}
                <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                  {insight.type}
                </span>
              </div>
              {getSignificanceBadge(insight.significance)}
            </div>

            <h3 className="font-semibold text-gray-900 mb-2">
              {insight.metric_involved}
            </h3>

            <p className="text-gray-600 mb-4 text-sm flex-grow">
              {insight.observation}
            </p>

            <div className="mt-auto bg-gray-50 p-3 rounded-lg text-sm text-gray-700 border-l-4 border-indigo-500">
              <span className="font-bold text-indigo-700 block mb-1 text-xs uppercase">
                Action:
              </span>
              {insight.actionable_advice}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Insights;
