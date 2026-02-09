import React, { useState } from "react";
import type {
  UserProfile,
  WeeklyPlanResponse,
  InsightsResponse,
} from "../types";
import { coachService } from "../services/api";
import UserProfileForm from "./UserProfileForm";
import WeeklyPlan from "./WeeklyPlan";
import Insights from "./Insights";
import { LayoutDashboard, Calendar, LineChart, LogOut } from "lucide-react";

const Dashboard: React.FC = () => {
  const [view, setView] = useState<"setup" | "plan" | "insights">("setup");
  const [weeklyPlan, setWeeklyPlan] = useState<WeeklyPlanResponse | null>(null);
  const [insights, setInsights] = useState<InsightsResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleProfileSubmit = async (userProfile: UserProfile) => {
    setIsLoading(true);
    setError(null);
    // setProfile(userProfile); // Could store profile if needed for other calls

    try {
      const planData = await coachService.generateWeeklyPlan(userProfile);
      setWeeklyPlan(planData);
      setView("plan");
    } catch (err) {
      setError("Failed to generate plan. Please try again.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTabChange = async (newView: "plan" | "insights") => {
    setView(newView);
    if (newView === "insights" && !insights) {
      setIsLoading(true);
      try {
        const insightsData = await coachService.getInsights(30);
        setInsights(insightsData);
      } catch (err) {
        setError("Failed to load insights.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const resetProfile = () => {
    setWeeklyPlan(null);
    setInsights(null);
    setView("setup");
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 px-4 py-3 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2 text-blue-600">
            <LayoutDashboard className="w-8 h-8" />
            <span className="text-xl font-bold tracking-tight">
              FitSense AI
            </span>
          </div>

          {view !== "setup" && (
            <div className="flex gap-4">
              <button
                onClick={() => handleTabChange("plan")}
                className={`flex items-center gap-2 px-3 py-2 rounded-md transition-colors ${
                  view === "plan"
                    ? "bg-blue-50 text-blue-700 font-medium"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <Calendar className="w-4 h-4" />
                Plan
              </button>
              <button
                onClick={() => handleTabChange("insights")}
                className={`flex items-center gap-2 px-3 py-2 rounded-md transition-colors ${
                  view === "insights"
                    ? "bg-blue-50 text-blue-700 font-medium"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <LineChart className="w-4 h-4" />
                Insights
              </button>
              <div className="h-8 w-px bg-gray-200 mx-2"></div>
              <button
                onClick={resetProfile}
                className="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 hover:text-red-600 hover:bg-red-50 transition-colors"
                title="Reset Profile"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-8">
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded shadow-sm animate-fadeIn">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {view === "setup" && (
          <div className="max-w-2xl mx-auto animate-fadeIn">
            <div className="text-center mb-10">
              <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
                Your AI Coach awaits.
              </h1>
              <p className="text-lg text-gray-600">
                Generate a fully personalized weekly workout plan based on your
                physiology and goals.
              </p>
            </div>
            <UserProfileForm
              onSubmit={handleProfileSubmit}
              isLoading={isLoading}
            />
          </div>
        )}

        {view === "plan" && weeklyPlan && <WeeklyPlan data={weeklyPlan} />}

        {view === "insights" &&
          (isLoading ? (
            <div className="flex flex-col items-center justify-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <p className="text-gray-500 font-medium">
                Analyzing historical data...
              </p>
            </div>
          ) : insights ? (
            <Insights data={insights} />
          ) : null)}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 flex justify-between items-center text-sm text-gray-500">
          <p>© 2024 FitSense AI. Hackathon Project.</p>
          <div className="flex gap-4">
            <span>Powered by Gemini 1.5</span>
            <span>&bull;</span>
            <span>Evaluated with Opik</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
