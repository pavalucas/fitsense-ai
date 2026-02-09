# FitSense AI

**The AI Coach that knows when to push you, and when to tell you to rest.**

FitSense AI is a context-aware fitness coaching platform that bridges the gap between raw wearable data and actionable training. Unlike static training plans, FitSense AI adapts your schedule in real-time based on your physiological recovery, stress levels, and long-term trends.

## 🚀 Key Features

-   **Dynamic Weekly Planning**: Generates bespoke 7-day training plans tailored to your goals (Muscle Gain, General Health, etc.), experience level, and available equipment.
-   **Real-time Daily Adaptation**: Automatically modifies planned workouts if high stress or elevated Resting Heart Rate (RHR) is detected via Garmin integration.
-   **AI-Powered Insights**: An `InsightsAgent` analyzes 30 days of history to find correlations (e.g., "Your RHR spikes 2 days after heavy Leg Days") and suggests actionable improvements.
-   **Garmin Integration**: Syncs live health metrics including Steps, Sleep, Heart Rate, Stress, and Activities.
-   **Mock Data Mode**: Full dashboard functionality available for users without a Garmin device.

## 🧠 Multi-Agent Architecture

FitSense AI is powered by **Google Gemini 1.5 Pro** using a specialized multi-agent system:

1.  **Planning Agent**: Constructs the initial weekly framework based on user profile and equipment.
2.  **Adaptation Agent**: Monitors daily recovery metrics to "downgrade" or "upgrade" sessions to prevent overtraining.
3.  **Analysis Agent**: Provides the "Why" behind every recommendation, explaining the logic of the AI coach.
4.  **Insights Agent**: Performs deep-dives into historical data to identify long-term patterns.

## 🛠️ Tech Stack

-   **Frontend**: Next.js, TypeScript, Tailwind CSS, Lucide React.
-   **Backend**: FastAPI (Python), Google Gemini 1.5 Pro.
-   **Observability & Safety**: **Opik** (Comet ML) for LLM evaluation, ensuring all coaching advice meets safety and specificity standards.
-   **Data**: Garmin Connect API integration.
-   **Deployment**: Vercel (Edge-ready).

## 🚦 Local Development

### Prerequisites

-   Python 3.9+
-   Node.js 18+
-   Google Gemini API Key

### 1. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your environment variables in a `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key
OPIK_API_KEY=your_opik_key (optional)
OPIK_WORKSPACE=your_workspace (optional)
```

Run the FastAPI server:
```bash
python main.py
```

### 2. Frontend Setup

Navigate to the `frontend` directory:

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`.

## 🛡️ Safety & Evaluation

We take physical safety seriously. Every prompt used in FitSense AI is rigorously tested against an evaluation suite powered by **Opik**. We measure:
-   **Safety Score**: Ensuring the AI doesn't recommend high-intensity work during injury or extreme fatigue.
-   **Specificity Score**: Ensuring the plans are tailored to the user's specific equipment and constraints.

## 📄 License

MIT

---
*Developed for the Commit to Change Hackathon.*