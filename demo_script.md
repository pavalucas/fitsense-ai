# FitSense AI - Hackathon Demo Script

**Tagline:** "The AI Coach that knows when to push you, and when to tell you to rest."

---

## 1. Introduction (0:00 - 0:30)
*   **Visual:** Slide with "FitSense AI" logo + tagline.
*   **Narrator:** "Generic fitness apps follow a rigid schedule. But life isn't rigid. FitSense AI is the first context-aware coaching platform that adapts your training in real-time based on your physiological recovery."
*   **Key Point:** "Powered by Google Gemini 1.5 and rigorously tested with Opik, it bridges the gap between raw data and actionable coaching."

## 2. Onboarding & Profiling (0:30 - 1:00)
*   **Visual:** Frontend `UserProfileForm` (The Setup Screen).
*   **Action:**
    *   Select "Intermediate".
    *   Select Goals: "Muscle Gain", "General Health".
    *   Select Equipment: "Dumbbells", "Bodyweight".
    *   **Click:** "Generate Weekly Plan".
*   **Narrator:** "We start by understanding the user. Not just age and weight, but specific equipment access and goals. Gemini takes this context to build a bespoke schedule."

## 3. The Intelligence: Weekly Planning (1:00 - 1:45)
*   **Visual:** `WeeklyPlan` Component (The Plan View).
*   **Action:** Scroll through the days. Hover over "Monday" or "Tuesday".
*   **Narrator:** "Here is our 7-day plan. Notice it's not just 'Run 5k'. It's structured: 'Upper Body Strength' on Tuesday, 'Active Recovery' on Monday because my recent stress levels were high. The AI explains *why* it chose this structure in the 'Analysis' section."
*   **Highlight:** Point out the `Recovery Status` banner (e.g., "Status: Moderate - Recommendation: Maintenance").

## 4. The "Magic" Moment: Daily Adaptation (1:45 - 2:30)
*   **Visual:** `Dashboard` (Daily Guidance / Adaptation View).
*   **Context:** "Imagine it's Wednesday. I have a 'High Intensity Interval' session planned."
*   **Scenario:**
    *   **Real-time Data:** My Garmin mock data shows **High Stress (75/100)** and **Elevated RHR (+5 bpm)** from a stressful workday.
    *   **The Problem:** Doing HIIT now would risk injury or burnout.
*   **Action:** Click "Get Daily Guidance".
*   **Result:** The AI detects the high stress/RHR and **changes** the workout.
*   **Visual:** "Modification Status: Modified". "Reason: High physiological stress detected. Intensity reduced to prevent overtraining."
*   **Narrator:** "This is the magic. FitSense detected my elevated stress and RHR. Instead of letting me burn out, it automatically downgraded the session to 'Steady State Cardio'. A static PDF plan would have broken me today; FitSense saved my recovery."

## 5. Long-term Context: Insights (2:30 - 3:00)
*   **Visual:** `Insights` Tab.
*   **Action:** Click "Insights" (Show loading spinner -> Results).
*   **Narrator:** "It doesn't just look at today. The `InsightsAgent` analyzes 30 days of history to find patterns."
*   **Example:** "Correlation: Your RHR spikes 2 days after heavy Leg Days. Recommendation: Add extra mobility work post-leg day."

## 6. Under the Hood: Gemini & Opik (3:00 - 3:30)
*   **Visual:** Slide or Screen Share of Code/Opik Dashboard.
*   **Narrator:** "We built this using a multi-agent architecture with **Google Gemini 1.5 Pro**. To ensure the advice is safe and helpful, we built a custom evaluation suite using **Opik**."
*   **Show:** Opik Dashboard showing "Safety Score: 1.0" and "Specificity Score: 0.9".
*   **Key Point:** "We don't guess. We evaluate. Every prompt is tested against scenarios like 'Injured Runner' or 'Overtrained Athlete' to guarantee safety."

## 7. Conclusion (3:30 - End)
*   **Visual:** FitSense AI Dashboard.
*   **Narrator:** "FitSense AI makes fitness data human. It's not just a tracker; it's a coach. Thank you."