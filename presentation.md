---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #2c3e50;
  }
  h2 {
    color: #34495e;
  }
  .highlight {
    color: #3498db;
    font-weight: bold;
  }

---

# FitSense AI
### The AI Coach that knows when to push you, and when to tell you to rest.

**Commit to Change Hackathon**

---

## 1. The Problem
- **Rigid Schedules:** Generic fitness apps follow fixed plans regardless of your life.
- **Data Fatigue:** Users have trackers (Garmin, Apple Watch) but don't know how to act on the data.
- **Overtraining:** Hard workouts when stressed lead to burnout or injury.

---

## 2. The Solution: FitSense AI
- **Context-Aware Coaching:** Adapts training in real-time based on physiological recovery.
- **Powered by Gemini 1.5 Pro:** Bridges the gap between raw data and actionable coaching.
- **Safety First:** Rigorously tested with **Opik** for reliable, safe advice.

---

## 3. Onboarding & Profiling
- **Bespoke Setup:** Not just age/weight.
- **Context Matters:**
  - Experience Level (e.g., Intermediate)
  - Goals (e.g., Muscle Gain, General Health)
  - Equipment (e.g., Dumbbells, Bodyweight)
- **Result:** A Gemini-generated weekly plan tailored to *your* reality.

---

## 4. Intelligence: Weekly Planning
- **Dynamic Scheduling:** 
  - *Example:* "Active Recovery" instead of "Sprints" if stress levels are high.
- **Transparent AI:** The "Analysis" section explains *why* a specific workout was chosen.
- **Recovery Status:** Continuous monitoring of your readiness.

---

## 5. The "Magic" Moment: Daily Adaptation
### Scenario: Wednesday HIIT Session Planned
- **Real-time Data:** Garmin detects High Stress (75/100) and Elevated RHR (+5 bpm).
- **The Adaptation:**
  - FitSense detects the physiological strain.
  - **Action:** Automatically downgrades HIIT to "Steady State Cardio."
  - **Benefit:** Prevents overtraining and injury before they happen.

---

## 6. Long-term Context: Insights
- **The InsightsAgent:** Goes beyond the daily view.
- **30-Day Analysis:** Identifies correlations between activities and recovery.
- **Actionable Advice:** 
  - *"Your RHR spikes 2 days after Leg Days. Suggestion: Add extra mobility work post-leg day."*

---

## 7. Under the Hood: Multi-Agent Architecture
- **Google Gemini 1.5 Pro:** The brain behind the planning and adaptation.
- **Garmin Integration:** Real-time physiological data ingestion.
- **Next.js & FastAPI:** Scalable frontend and backend integration.

---

## 8. Quality & Safety with Opik
- **Evaluation Suite:** We don't guess; we measure.
- **Custom Metrics:**
  - **Safety Score:** Ensuring advice isn't dangerous.
  - **Specificity Score:** Ensuring plans aren't generic.
- **Tested Scenarios:** "Injured Runner," "Overtrained Athlete," "Traveler with no equipment."

---

## 9. Conclusion
### FitSense AI makes fitness data human.

- **Adaptive**
- **Safe**
- **Personalized**

**Thank you!**
