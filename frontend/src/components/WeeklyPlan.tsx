import React from "react";
import type { WeeklyPlanResponse, DailyPlan } from "../types";
import { Activity, Clock, Calendar, Dumbbell } from "lucide-react";

interface WeeklyPlanProps {
  data: WeeklyPlanResponse;
}

const WeeklyPlan: React.FC<WeeklyPlanProps> = ({ data }) => {
  const { recovery_analysis, weekly_plan } = data;

  // Helper for intensity colors
  const getIntensityColor = (intensity: string) => {
    switch (intensity.toLowerCase()) {
      case "low":
        return "bg-green-100 text-green-800";
      case "moderate":
        return "bg-yellow-100 text-yellow-800";
      case "high":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  // Helper for recovery status colors
  const getRecoveryColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "poor":
        return "bg-red-50 border-red-200 text-red-900";
      case "moderate":
        return "bg-yellow-50 border-yellow-200 text-yellow-900";
      case "good":
      case "excellent":
        return "bg-green-50 border-green-200 text-green-900";
      default:
        return "bg-blue-50 border-blue-200 text-blue-900";
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Recovery Status Banner */}
      <div
        className={`p-6 rounded-lg border ${getRecoveryColor(
          recovery_analysis.recovery_status,
        )} shadow-sm`}
      >
        <div className="flex items-start gap-4">
          <Activity className="w-8 h-8 mt-1 opacity-80" />
          <div className="flex-1">
            <h3 className="font-bold text-xl capitalize flex items-center gap-2">
              Current Status: {recovery_analysis.recovery_status}
              <span className="text-sm font-normal px-2 py-0.5 bg-white/50 rounded-full border border-black/5">
                Score: {recovery_analysis.recovery_score}
              </span>
            </h3>
            <p className="mt-2 text-lg font-medium">
              Recommendation: {recovery_analysis.recommendation.action}
            </p>
            <p className="text-sm mt-1 opacity-90">
              {recovery_analysis.recommendation.advice}
            </p>
            <div className="mt-4 pt-4 border-t border-black/10 text-sm">
              <span className="font-semibold">Analysis:</span>{" "}
              {recovery_analysis.reasoning}
            </div>
          </div>
        </div>
      </div>

      {/* Week Summary */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <h2 className="text-2xl font-bold mb-3 flex items-center gap-2 text-gray-800">
          <Calendar className="w-6 h-6 text-blue-600" />
          Weekly Focus
        </h2>
        <p className="text-gray-700 text-lg leading-relaxed">
          {weekly_plan.week_summary}
        </p>
      </div>

      {/* Daily Plans Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {weekly_plan.daily_plans.map((dayPlan: DailyPlan, index: number) => (
          <div
            key={index}
            className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 border border-gray-100 flex flex-col"
          >
            {/* Header */}
            <div className="bg-gray-50 p-4 border-b border-gray-100">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-bold text-lg text-gray-900">
                  {dayPlan.day}
                </h3>
                <span
                  className={`px-2 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${getIntensityColor(
                    dayPlan.intensity,
                  )}`}
                >
                  {dayPlan.intensity}
                </span>
              </div>
              <div className="text-blue-700 font-semibold mb-1">
                {dayPlan.workout_type}
              </div>
              <div className="flex items-center gap-1.5 text-sm text-gray-500">
                <Clock className="w-4 h-4" />
                {dayPlan.estimated_duration} mins
              </div>
            </div>

            {/* Content */}
            <div className="p-4 flex-1 flex flex-col">
              {dayPlan.focus && (
                <div className="mb-4 text-sm bg-blue-50 text-blue-800 p-2 rounded">
                  <span className="font-semibold">Focus:</span> {dayPlan.focus}
                </div>
              )}

              <h4 className="font-semibold text-sm text-gray-700 mb-3 flex items-center gap-1.5">
                <Dumbbell className="w-4 h-4" /> Exercises
              </h4>

              {dayPlan.exercises && dayPlan.exercises.length > 0 ? (
                <ul className="space-y-3 flex-1">
                  {dayPlan.exercises.map((exercise, i) => (
                    <li
                      key={i}
                      className="text-sm border-b border-gray-50 last:border-0 pb-2 last:pb-0"
                    >
                      <div className="font-medium text-gray-900">
                        {exercise.name}
                      </div>
                      <div className="text-gray-500 text-xs mt-0.5 flex flex-wrap gap-2">
                        {exercise.sets && (
                          <span className="bg-gray-100 px-1.5 py-0.5 rounded text-gray-600">
                            {exercise.sets} sets
                          </span>
                        )}
                        {exercise.reps && (
                          <span className="bg-gray-100 px-1.5 py-0.5 rounded text-gray-600">
                            {exercise.reps} reps
                          </span>
                        )}
                        {exercise.rest_seconds && (
                          <span className="text-gray-400">
                            {exercise.rest_seconds}s rest
                          </span>
                        )}
                      </div>
                      {exercise.notes && (
                        <div className="text-xs text-gray-400 mt-1 italic">
                          "{exercise.notes}"
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="flex-1 flex items-center justify-center text-gray-400 text-sm italic py-4">
                  Recovery / Rest
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeeklyPlan;
