export interface UserProfile {
  fitness_level: 'Beginner' | 'Intermediate' | 'Advanced';
  goals: string[];
  equipment: string[];
  limitations?: string[];
}

export interface Exercise {
  name: string;
  sets?: number;
  reps?: string | number;
  rest_seconds?: number;
  notes?: string;
}

export interface DailyPlan {
  day: string;
  workout_type: string;
  focus?: string;
  exercises: Exercise[];
  estimated_duration: number;
  intensity: 'Low' | 'Moderate' | 'High';
}

export interface WeeklyPlan {
  week_summary: string;
  daily_plans: DailyPlan[];
}

export interface RecoveryMetricsSummary {
  body_battery?: string;
  sleep_quality?: string;
  stress_level?: string;
  rhr_trend?: string;
}

export interface RecoveryRecommendation {
  action: string;
  intensity_level: string;
  advice: string;
}

export interface RecoveryAnalysis {
  recovery_status: 'poor' | 'moderate' | 'good' | 'excellent';
  recovery_score: number;
  key_metrics_summary: RecoveryMetricsSummary;
  trends_identified: string[];
  recommendation: RecoveryRecommendation;
  reasoning: string;
}

export interface WeeklyPlanResponse {
  status: string;
  recovery_analysis: RecoveryAnalysis;
  weekly_plan: WeeklyPlan;
}

// Daily Guidance Types

export interface ScheduledWorkout {
  workout_type: string;
  intensity: string;
  duration_min: number;
  exercises?: string[];
  notes?: string;
}

export interface SafetyCheck {
  passed: boolean;
  concerns: string[];
}

export interface AdaptationResult {
  modification_status: 'unchanged' | 'modified' | 'cancelled_for_rest' | 'error';
  adaptation_reason: string;
  safety_check: SafetyCheck;
  original_workout_summary?: string;
  adapted_workout: ScheduledWorkout | any;
}

export interface DailyGuidanceResponse {
  date: string;
  recovery_status: RecoveryAnalysis;
  guidance_type: 'general' | 'workout_adaptation';
  adaptation?: AdaptationResult;
}

// Insights Types

export interface Insight {
  type: 'correlation' | 'trend' | 'anomaly';
  metric_involved: string;
  observation: string;
  significance: 'High' | 'Medium' | 'Low';
  actionable_advice: string;
}

export interface InsightsResponse {
  insights: Insight[];
  summary: string;
}
