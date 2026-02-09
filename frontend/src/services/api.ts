import axios from "axios";
import type {
  UserProfile,
  WeeklyPlanResponse,
  DailyGuidanceResponse,
  ScheduledWorkout,
  InsightsResponse,
} from "../types";

// Use environment variable or default to localhost (for development)
// On Vercel, we use relative paths as the API is proxied via vercel.json
const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? "http://localhost:8000" : "");

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const coachService = {
  /**
   * Generate a weekly workout plan based on user profile.
   */
  generateWeeklyPlan: async (
    userProfile: UserProfile,
  ): Promise<WeeklyPlanResponse> => {
    try {
      const response = await api.post<WeeklyPlanResponse>(
        "/api/coach/plan",
        userProfile,
      );
      return response.data;
    } catch (error) {
      console.error("Error generating weekly plan:", error);
      throw error;
    }
  },

  /**
   * Get daily guidance, optionally adapting a scheduled workout.
   */
  getDailyGuidance: async (
    scheduledWorkout?: ScheduledWorkout,
  ): Promise<DailyGuidanceResponse> => {
    try {
      // payload matches DailyGuidanceRequest in backend
      const payload = scheduledWorkout
        ? { scheduled_workout: scheduledWorkout }
        : {};
      const response = await api.post<DailyGuidanceResponse>(
        "/api/coach/daily",
        payload,
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching daily guidance:", error);
      throw error;
    }
  },

  /**
   * Get insights from historical data.
   */
  getInsights: async (daysBack: number = 30): Promise<InsightsResponse> => {
    try {
      const response = await api.get<InsightsResponse>(`/api/coach/insights`, {
        params: { days: daysBack },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching insights:", error);
      throw error;
    }
  },
};
