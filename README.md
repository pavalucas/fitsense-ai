# FitSense AI

FitSense AI is a health analytics dashboard that integrates with Garmin to provide AI-powered insights into recovery, training readiness, and sleep quality.

## Features

-   **Garmin Integration**: Syncs real data (Steps, Sleep, Heart Rate, Activities) using Garmin credentials.
-   **Mock Data Mode**: Explore the dashboard without a Garmin account.
-   **Dashboard**: Visualizes key health metrics and weekly activity trends.
-   **Privacy Focused**: Runs locally or deployable to Vercel.

## Local Development

### Prerequisites

-   Python 3.9+
-   Node.js 18+

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend application will be available at `http://localhost:5173`.

## Environment Variables (Optional)

You can create a `.env` file in the `backend/` directory to pre-configure Garmin credentials, though the UI also allows logging in directly.

```env
GARMIN_EMAIL=your_email@example.com
GARMIN_PASSWORD=your_password
GARMIN_DISPLAY_NAME=your_display_name (optional)
```

## Deployment

This project is configured for deployment on Vercel.

1.  Push code to GitHub.
2.  Import project into Vercel.
3.  Vercel will automatically detect the `vercel.json` configuration and deploy both frontend and backend.
