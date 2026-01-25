import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Activity,
  Moon,
  Heart,
  Flame,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Dumbbell,
  Timer,
  TrendingUp,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";

// --- Types ---

interface GarminStatus {
  message: string;
  garmin_status: string;
}

interface GarminSummary {
  date: string;
  sleep_score: number;
  total_sleep_minutes: number;
  resting_heart_rate: number;
  steps: number;
  active_minutes: number;
  calories_burned: number;
}

interface GarminActivity {
  activity_type: string;
  start_time: string;
  duration_minutes: number;
  distance_km?: number;
  avg_hr?: number;
}

interface SyncResponse {
  user_id: string;
  period: string;
  synced_days: number;
  activities_count: number;
  status: string;
  sample_data: {
    latest_summary: GarminSummary | null;
    latest_activity: GarminActivity | null;
  };
}

// --- Configuration ---

// In production (Vercel), /api points to the backend.
// Locally, we might need the full URL if not proxied, but CORS is enabled.
const API_BASE_URL = import.meta.env.PROD ? "" : "http://localhost:8000";

function App() {
  const [status, setStatus] = useState<GarminStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [syncData, setSyncData] = useState<SyncResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Mock data for the chart to demonstrate visualization capabilities
  // since the current hackathon backend checkpoint returns mostly summary stats
  const [chartData] = useState([
    { name: "Mon", steps: 6500, sleep: 420 },
    { name: "Tue", steps: 8200, sleep: 380 },
    { name: "Wed", steps: 10500, sleep: 450 },
    { name: "Thu", steps: 7800, sleep: 410 },
    { name: "Fri", steps: 9200, sleep: 390 },
    { name: "Sat", steps: 12000, sleep: 500 },
    { name: "Sun", steps: 5000, sleep: 520 },
  ]);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/`);
      setStatus(res.data);
    } catch (err) {
      console.error(err);
      setStatus({ message: "Backend unreachable", garmin_status: "Offline" });
    }
  };

  const handleSync = async () => {
    setLoading(true);
    setError(null);
    try {
      // Demo user ID
      const res = await axios.get<SyncResponse>(
        `${API_BASE_URL}/api/garmin/sync/demo_user`,
      );
      setSyncData(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to sync data. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans selection:bg-blue-500 selection:text-white">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-blue-500" />
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              FitSense AI
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <span
              className={`px-3 py-1 rounded-full text-xs font-medium border ${
                status?.garmin_status === "Authenticated"
                  ? "bg-green-500/10 border-green-500/50 text-green-400"
                  : "bg-yellow-500/10 border-yellow-500/50 text-yellow-400"
              }`}
            >
              {status?.garmin_status || "Checking..."}
            </span>
            <a
              href="https://github.com/your-team/project"
              target="_blank"
              rel="noreferrer"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              GitHub
            </a>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Welcome / Actions Section */}
        <div className="mb-12 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Your Health,{" "}
            <span className="text-blue-500">Intelligently Analyzed</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto mb-8">
            Sync your Garmin data to get AI-powered insights into your recovery,
            training readiness, and sleep quality.
          </p>

          <button
            onClick={handleSync}
            disabled={loading}
            className={`
              group relative inline-flex items-center justify-center px-8 py-3
              text-base font-medium text-white bg-blue-600 rounded-full
              hover:bg-blue-700 transition-all duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
              shadow-lg shadow-blue-500/30
            `}
          >
            {loading ? (
              <RefreshCw className="h-5 w-5 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="h-5 w-5 mr-2 group-hover:rotate-180 transition-transform duration-500" />
            )}
            {loading ? "Syncing..." : "Sync Garmin Data"}
          </button>

          {error && (
            <div className="mt-4 flex items-center justify-center text-red-400 space-x-2">
              <AlertCircle className="h-4 w-4" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Dashboard Content */}
        {syncData && (
          <div className="space-y-8 animate-fade-in">
            {/* Sync Status Banner */}
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-4 flex flex-col md:flex-row items-center justify-between">
              <div className="flex items-center space-x-3 mb-2 md:mb-0">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <div>
                  <p className="font-medium text-white">
                    Data Synchronization Complete
                  </p>
                  <p className="text-sm text-gray-400">
                    Synced {syncData.synced_days} days of data •{" "}
                    {syncData.activities_count} activities found
                  </p>
                </div>
              </div>
              <div className="text-xs text-gray-500 font-mono">
                ID: {syncData.user_id}
              </div>
            </div>

            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Sleep Metric */}
              <StatsCard
                icon={<Moon className="h-6 w-6 text-purple-400" />}
                title="Sleep Score"
                value={
                  syncData.sample_data.latest_summary?.sleep_score?.toString() ||
                  "N/A"
                }
                unit="/ 100"
                trend="Good"
                color="purple"
              />

              {/* Steps Metric */}
              <StatsCard
                icon={<TrendingUp className="h-6 w-6 text-blue-400" />}
                title="Daily Steps"
                value={
                  syncData.sample_data.latest_summary?.steps?.toLocaleString() ||
                  "0"
                }
                unit="steps"
                trend="+12% vs avg"
                color="blue"
              />

              {/* RHR Metric */}
              <StatsCard
                icon={<Heart className="h-6 w-6 text-red-400" />}
                title="Resting HR"
                value={
                  syncData.sample_data.latest_summary?.resting_heart_rate?.toString() ||
                  "N/A"
                }
                unit="bpm"
                trend="Stable"
                color="red"
              />

              {/* Calories Metric */}
              <StatsCard
                icon={<Flame className="h-6 w-6 text-orange-400" />}
                title="Active Calories"
                value={
                  syncData.sample_data.latest_summary?.calories_burned?.toString() ||
                  "0"
                }
                unit="kcal"
                trend="High"
                color="orange"
              />
            </div>

            {/* Charts & Details Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Chart */}
              <div className="lg:col-span-2 bg-gray-800 rounded-2xl p-6 border border-gray-700 shadow-xl">
                <h3 className="text-lg font-semibold mb-6 flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-gray-400" />
                  Weekly Activity Trends
                </h3>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#374151"
                        vertical={false}
                      />
                      <XAxis
                        dataKey="name"
                        stroke="#9CA3AF"
                        tickLine={false}
                        axisLine={false}
                      />
                      <YAxis
                        stroke="#9CA3AF"
                        tickLine={false}
                        axisLine={false}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#1F2937",
                          borderColor: "#374151",
                          color: "#F3F4F6",
                        }}
                        itemStyle={{ color: "#F3F4F6" }}
                      />
                      <Bar
                        dataKey="steps"
                        fill="#3B82F6"
                        radius={[4, 4, 0, 0]}
                        name="Steps"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Latest Activity Card */}
              <div className="bg-gray-800 rounded-2xl p-6 border border-gray-700 shadow-xl flex flex-col">
                <h3 className="text-lg font-semibold mb-6 flex items-center">
                  <Dumbbell className="h-5 w-5 mr-2 text-gray-400" />
                  Latest Workout
                </h3>

                {syncData.sample_data.latest_activity ? (
                  <div className="flex-1 flex flex-col justify-center">
                    <div className="flex items-center justify-between mb-6">
                      <div className="p-3 bg-gray-700 rounded-lg">
                        <Activity className="h-8 w-8 text-green-400" />
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-400">
                          {formatDate(
                            syncData.sample_data.latest_activity.start_time,
                          )}
                        </p>
                        <p className="font-bold text-xl capitalize">
                          {syncData.sample_data.latest_activity.activity_type.replace(
                            "_",
                            " ",
                          )}
                        </p>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                        <span className="text-gray-400 flex items-center">
                          <Timer className="h-4 w-4 mr-2" /> Duration
                        </span>
                        <span className="font-medium">
                          {Math.round(
                            syncData.sample_data.latest_activity
                              .duration_minutes,
                          )}{" "}
                          min
                        </span>
                      </div>

                      {syncData.sample_data.latest_activity.distance_km && (
                        <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                          <span className="text-gray-400 flex items-center">
                            <TrendingUp className="h-4 w-4 mr-2" /> Distance
                          </span>
                          <span className="font-medium">
                            {syncData.sample_data.latest_activity.distance_km.toFixed(
                              2,
                            )}{" "}
                            km
                          </span>
                        </div>
                      )}

                      {syncData.sample_data.latest_activity.avg_hr && (
                        <div className="flex justify-between items-center p-3 bg-gray-700/50 rounded-lg">
                          <span className="text-gray-400 flex items-center">
                            <Heart className="h-4 w-4 mr-2" /> Avg HR
                          </span>
                          <span className="font-medium">
                            {syncData.sample_data.latest_activity.avg_hr} bpm
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="flex-1 flex items-center justify-center text-gray-500">
                    No recent activity found
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Empty State / Initial Placeholder */}
        {!syncData && !loading && (
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 opacity-50">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-48 rounded-2xl bg-gray-800 border border-gray-700 animate-pulse"
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

// Stats Card Component
const StatsCard = ({ icon, title, value, unit, trend, color }: any) => {
  return (
    <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg hover:border-gray-600 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-2 rounded-lg bg-${color}-500/10`}>{icon}</div>
        {/* Optional Trend Indicator */}
        {trend && (
          <span className="text-xs font-medium px-2 py-1 rounded bg-gray-700 text-gray-300">
            {trend}
          </span>
        )}
      </div>
      <h3 className="text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <div className="flex items-baseline">
        <span className="text-2xl font-bold text-white mr-1">{value}</span>
        <span className="text-sm text-gray-500">{unit}</span>
      </div>
    </div>
  );
};

export default App;
