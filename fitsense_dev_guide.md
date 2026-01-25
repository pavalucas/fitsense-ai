# FitSense AI - Complete Development Guide

## Project Overview

**Project Name:** FitSense AI - Your Adaptive Fitness Coach

**Prize Targets:**
1. Best Use of Opik ($5,000)
2. Health, Fitness & Wellness ($5,000)

**Tech Stack:**
- Backend: Python 3.11 + FastAPI
- Frontend: React + TypeScript + Tailwind CSS
- Database: PostgreSQL 15
- LLM: Anthropic Claude (Sonnet 4)
- Observability: Opik
- External APIs: Garmin Connect API
- Deployment: Docker + Docker Compose

**Core Value Proposition:**
An AI fitness coach that automatically syncs with Garmin devices to deliver truly personalized workout plans that adapt daily based on real-time recovery data (Body Battery, sleep, stress, HRV). Uses comprehensive Opik evaluation to ensure safe, effective, evidence-based coaching.

---

## Complete Project Structure

```
fitsense-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── workout.py
│   │   │   ├── garmin_data.py
│   │   │   └── coaching_session.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── garmin.py
│   │   │   ├── coach.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── garmin_service.py
│   │   │   ├── ai_agents/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_agent.py
│   │   │   │   ├── data_sync_agent.py
│   │   │   │   ├── analysis_agent.py
│   │   │   │   ├── planning_agent.py
│   │   │   │   ├── adaptation_agent.py
│   │   │   │   └── insights_agent.py
│   │   │   ├── opik_service.py
│   │   │   └── evaluation/
│   │   │       ├── __init__.py
│   │   │       ├── evaluators.py
│   │   │       ├── test_scenarios.py
│   │   │       └── metrics.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── prompts.py
│   │       └── validators.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_agents.py
│   │   ├── test_garmin.py
│   │   └── test_evaluations.py
│   ├── alembic/
│   │   └── versions/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── GarminConnect.tsx
│   │   │   ├── WorkoutPlan.tsx
│   │   │   ├── RecoveryStatus.tsx
│   │   │   ├── BodyComposition.tsx
│   │   │   ├── CoachChat.tsx
│   │   │   └── OpikDashboard.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docs/
│   ├── OPIK_SHOWCASE.md
│   ├── ARCHITECTURE.md
│   └── DEMO_SCRIPT.md
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## PHASE 1: Project Initialization & Setup

### Step 1.1: Create Project Repository
- Initialize Git repository
- Create .gitignore (exclude .env, node_modules, __pycache__, venv)
- Create initial README.md with project description
- Set up GitHub repository (public for hackathon)

### Step 1.2: Backend Configuration Files

**backend/requirements.txt:**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
anthropic==0.18.1
opik==0.2.0
httpx==0.26.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
garth==0.4.46
pytest==7.4.4
pytest-asyncio==0.23.3
python-dateutil==2.8.2
```

**backend/.env.example:**
```
DATABASE_URL=postgresql://fitsense:fitsense_password@db:5432/fitsense_db
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPIK_API_KEY=your_opik_api_key_here
OPIK_WORKSPACE=fitsense-workspace
GARMIN_CONSUMER_KEY=your_garmin_consumer_key
GARMIN_CONSUMER_SECRET=your_garmin_consumer_secret
GARMIN_OAUTH_CALLBACK=http://localhost:8000/api/garmin/callback
SECRET_KEY=generate_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200
ENVIRONMENT=development
DEBUG=True
```

**backend/Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: fitsense
      POSTGRES_PASSWORD: fitsense_password
      POSTGRES_DB: fitsense_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fitsense"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000

volumes:
  postgres_data:
```

### Step 1.3: Frontend Configuration

**frontend/package.json:**
```json
{
  "name": "fitsense-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "recharts": "^2.10.0",
    "axios": "^1.6.0",
    "date-fns": "^2.30.0",
    "lucide-react": "^0.292.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

**frontend/Dockerfile:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
```

**frontend/tailwind.config.js:**
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

---

## PHASE 2: Database Schema & Models

### Step 2.1: Database Configuration

**backend/app/config.py:**
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # API Keys
    ANTHROPIC_API_KEY: str
    OPIK_API_KEY: str
    OPIK_WORKSPACE: str
    
    # Garmin
    GARMIN_CONSUMER_KEY: str
    GARMIN_CONSUMER_SECRET: str
    GARMIN_OAUTH_CALLBACK: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    
    # App
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**backend/app/database.py:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import app.models.user
    import app.models.garmin_data
    import app.models.workout
    import app.models.coaching_session
    Base.metadata.create_all(bind=engine)
```

### Step 2.2: Define All Database Models

**backend/app/models/user.py:**
Define User model with fields:
- id, email, hashed_password, full_name, created_at
- Fitness profile: fitness_level, primary_goal, weekly_workout_target
- Garmin tokens: garmin_access_token, garmin_access_secret, garmin_user_id, garmin_last_sync
- Relationships to garmin_data, workouts, coaching_sessions

**backend/app/models/garmin_data.py:**
Define two models:
1. GarminData (daily summary):
   - Sleep metrics: sleep_score, total_sleep_minutes, deep/light/rem/awake minutes
   - Recovery: body_battery, stress_score, resting_heart_rate, hrv
   - Activity: steps, active_minutes, calories_burned
   - Body composition: weight_kg, body_fat_percentage, muscle_mass_kg
   - raw_data (JSON for full Garmin response)

2. GarminActivity (individual workouts):
   - activity_type, start_time, duration_minutes
   - Running: distance_km, avg_pace, avg_hr, max_hr, elevation_gain, vo2_max
   - Strength: exercise_count, set_count
   - Training effect metrics
   - raw_data (JSON)

**backend/app/models/workout.py:**
Define two models:
1. Workout (individual planned/completed workouts):
   - scheduled_date, completed, completed_at
   - workout_type, title, description
   - AI generated: exercises (JSON), target_duration, target_intensity
   - Actual completion: actual_duration, actual_exercises, perceived_exertion
   - AI context: generation_context, adaptation_reason

2. WeeklyPlan (weekly workout overview):
   - week_start_date, week_end_date
   - plan_summary, focus_areas (JSON)
   - AI metadata: model_version, prompt_version

**backend/app/models/coaching_session.py:**
Define CoachingSession model:
- session_type (analysis, planning, adaptation, insight, chat)
- user_message, context_data (JSON)
- agent_type, agent_response, reasoning
- Opik tracking: opik_trace_id, opik_span_id
- evaluation_scores (JSON)
- Performance: model_used, tokens_used, latency_ms

### Step 2.3: Initialize Database

**backend/app/main.py:**
Create FastAPI app with:
- CORS middleware
- Database initialization on startup
- API router inclusion
- Health check endpoint
- Root endpoint with API info

---

## PHASE 3: Authentication System

### Step 3.1: Implement JWT Authentication

**backend/app/api/auth.py:**
Implement:
- Password hashing utilities (bcrypt)
- JWT token creation and validation
- OAuth2 password bearer scheme
- get_current_user dependency
- POST /register endpoint (create new user)
- POST /login endpoint (return JWT token)
- GET /me endpoint (get current user info)

### Step 3.2: Secure API Routes

Add authentication dependency to all protected routes:
- All /api/garmin/* routes
- All /api/coach/* routes
- All /api/analytics/* routes

---

## PHASE 4: Garmin Integration (CRITICAL FEATURE)

### Step 4.1: Garmin Service Implementation

**backend/app/services/garmin_service.py:**

Implement GarminService class with methods:

1. **get_oauth_url()**: Generate OAuth authorization URL
2. **exchange_token(oauth_token, oauth_verifier)**: Exchange OAuth tokens for access tokens
3. **get_daily_summary(access_token, access_secret, date)**: Fetch sleep, wellness, activity for a day
4. **get_activities(access_token, access_secret, start_date, end_date)**: Fetch workouts in date range
5. **get_body_composition(access_token, access_secret, start_date, end_date)**: Fetch weight/body fat data
6. **sync_user_data(user_id, access_token, access_secret, days_back)**: Complete sync operation

Key considerations:
- Use garth library for Garmin API interaction
- Handle OAuth token refresh
- Parse Garmin API responses into standardized format
- Error handling for API rate limits, auth failures
- Logging for debugging

### Step 4.2: Garmin API Endpoints

**backend/app/api/garmin.py:**

Implement endpoints:

1. **GET /api/garmin/connect**: Initiate OAuth flow, return authorization URL
2. **GET /api/garmin/callback**: Handle OAuth callback, store tokens
3. **POST /api/garmin/sync**: Manually trigger sync (specify days_back)
4. **GET /api/garmin/status**: Check connection status and last sync time
5. **DELETE /api/garmin/disconnect**: Revoke tokens and disconnect

For sync endpoint:
- Fetch data from Garmin
- Parse and validate
- Store in GarminData and GarminActivity tables
- Use merge/upsert to handle duplicates
- Return summary of synced data

### Step 4.3: Background Sync (Optional but Recommended)

Implement daily automatic sync:
- Use APScheduler or Celery
- Run at 6 AM daily for all connected users
- Sync last 2 days of data
- Handle failures gracefully
- Log sync status

---

## PHASE 5: AI Agent System (CORE INTELLIGENCE)

### Step 5.1: Base Agent Architecture

**backend/app/services/ai_agents/base_agent.py:**

Create BaseAgent class with:
- Anthropic client initialization
- Opik client initialization
- run() method with Opik tracking decorator
- _build_system_prompt() (override in subclasses)
- _format_user_message() (add context)
- _extract_reasoning() (parse agent thought process)

Key features:
- Automatic Opik tracing for every agent call
- Log input, output, metadata, latency
- Structured error handling
- Token usage tracking

### Step 5.2: Specialized Agents

**1. AnalysisAgent** (backend/app/services/ai_agents/analysis_agent.py):

Purpose: Analyze recovery status from Garmin data

Methods:
- analyze_recovery_status(garmin_data): Takes 7-14 days of data, returns recovery assessment

System prompt includes:
- Recovery metric interpretations (Body Battery, sleep score, stress, RHR, HRV)
- Pattern recognition guidelines
- Overtraining signal detection
- Evidence-based decision rules

Output format:
- Current recovery status (poor/moderate/good/excellent)
- Key metrics summary
- Trends identified
- Recommendation for today's intensity
- Reasoning/evidence

**2. PlanningAgent** (backend/app/services/ai_agents/planning_agent.py):

Purpose: Generate weekly workout plans

Methods:
- generate_weekly_plan(user_profile, recent_workouts, recovery_status): Create 7-day plan

System prompt includes:
- User goals and fitness level
- Exercise science principles (progressive overload, specificity, recovery)
- Exercise library access instructions
- Structured output format (JSON)

Output format:
```json
{
  "week_summary": "Focus on building base endurance and upper body strength",
  "daily_plans": [
    {
      "day": "Monday",
      "workout_type": "strength_upper",
      "exercises": [
        {"name": "Bench Press", "sets": 4, "reps": 8, "rest_seconds": 90},
        ...
      ],
      "estimated_duration": 45,
      "intensity": "moderate"
    },
    ...
  ]
}
```

**3. AdaptationAgent** (backend/app/services/ai_agents/adaptation_agent.py):

Purpose: Modify today's workout based on current recovery

Methods:
- adapt_workout(scheduled_workout, today_recovery, recent_training_load): Adjust or maintain workout

System prompt includes:
- Current recovery data
- Scheduled workout details
- Adaptation guidelines (when to rest, reduce, maintain, push)
- Safety-first approach

Decision matrix:
- Body Battery <30 + Sleep <60 → Rest or very light
- Body Battery 30-50 → Reduce intensity 1-2 levels
- Stress >70 + elevated RHR → Active recovery
- Good recovery → Proceed as planned

Output:
- Adapted workout (if changed)
- Adaptation reason
- Safety check passed/failed

**4. InsightsAgent** (backend/app/services/ai_agents/insights_agent.py):

Purpose: Find patterns and generate actionable insights

Methods:
- generate_insights(historical_data, timeframe): Analyze long-term trends

System prompt includes:
- Pattern recognition techniques
- Correlation analysis instructions
- Example insights format

Output examples:
- "Your running pace improves 15s/km when Body Battery >75"
- "Sleep quality drops after leg day - consider earlier in week"
- "Resting HR decreased 3bpm this month = fitness improving"

### Step 5.3: Agent Orchestration

**backend/app/services/coach_orchestrator.py:**

Create CoachOrchestrator class to coordinate agents:
- Determine which agent(s) to call based on user request
- Manage multi-agent workflows
- Aggregate results
- Handle fallbacks

Example workflow for "generate this week's plan":
1. AnalysisAgent → Assess current recovery
2. PlanningAgent → Generate base plan
3. AdaptationAgent → Adjust Monday based on today's data
4. Return complete plan

---

## PHASE 6: Opik Evaluation System (CRITICAL FOR PRIZE)

### Step 6.1: Evaluation Metrics Implementation

**backend/app/services/evaluation/evaluators.py:**

Implement 7+ evaluator classes:

**1. RecoveryAssessmentEvaluator:**
- Uses LLM-as-judge to score recovery interpretation accuracy
- Evaluates if agent correctly identified recovery signals
- Checks if recommendation aligns with data
- Score 0.0-1.0

**2. SafetyEvaluator:**
- Checks for unsafe workout recommendations
- Red flags: High intensity when exhausted, volume spikes >20%, inadequate recovery
- Automatic 0.0 for serious safety violations
- Score weighted heavily in overall

**3. PersonalizationEvaluator:**
- Assesses how well coaching uses user-specific data
- Checks for references to user's goals, history, preferences
- Penalizes generic advice
- Score based on data-driven specificity

**4. TrainingLoadBalanceEvaluator:**
- Rule-based evaluation of weekly volume changes
- Ideal: -10% to +10% change week-over-week
- Acceptable: -20% to +15%
- Poor: >20% increase (injury risk)

**5. EvidenceBasedEvaluator:**
- Checks if recommendations align with exercise science
- Validates rest periods, rep ranges, progression rates
- Flags pseudoscience or broscience

**6. CommunicationQualityEvaluator:**
- Assesses clarity, tone, actionability
- Checks for appropriate caveats and disclaimers
- Evaluates motivation without toxicity

**7. GoalAlignmentEvaluator:**
- Verifies recommendations support user's stated goals
- Strength goal → appropriate strength programming
- Running goal → specific pace/distance targets

**CompositeCoachEvaluator:**
- Runs all evaluators
- Weighted average (Safety 40%, Recovery 25%, Personalization 20%, others 15%)
- Returns individual and overall scores

### Step 6.2: Test Scenario Library

**backend/app/services/evaluation/test_scenarios.py:**

Create comprehensive test scenarios for each dimension:

**Recovery Assessment Scenarios (10+ cases):**
- Poor recovery (BB <30, sleep <60) → should recommend rest
- Moderate recovery → reduce intensity
- Good recovery → proceed as planned
- Overtraining signals → flag concern
- Mixed signals → conservative approach

**Safety Scenarios (10+ cases):**
- Volume spike >25% → should fail
- High intensity with poor recovery → should fail
- Appropriate progression → should pass
- Back-to-back hard sessions on same muscle group → should fail

**Personalization Scenarios (10+ cases):**
- Generic response test → low score
- Data-specific response test → high score
- Goal misalignment → low score

Store scenarios with:
- scenario_id
- description
- input_data
- expected_output or expected_behavior
- pass/fail criteria

### Step 6.3: Opik Service Integration

**backend/app/services/opik_service.py:**

Implement OpikService class:

1. **log_coaching_interaction()**: Log every agent call to Opik
2. **evaluate_interaction()**: Run evaluators on coaching session
3. **run_regression_tests()**: Execute all test scenarios
4. **create_experiment()**: Set up A/B test in Opik
5. **log_experiment_result()**: Record experiment metrics
6. **get_evaluation_summary()**: Fetch scores over time

Use Opik features:
- Traces for individual interactions
- Spans for multi-step workflows
- Experiments for A/B tests
- Datasets for test scenarios
- Dashboards for visualization

### Step 6.4: Automated Testing Integration

Run regression tests:
- On every deployment
- Daily via cron job
- Before prompt changes
- Store results in Opik
- Alert on score degradation >5%

---

## PHASE 7: Coach API Endpoints

### Step 7.1: Core Coach Endpoints

**backend/app/api/coach.py:**

Implement:

**POST /api/coach/analyze-recovery:**
- Fetch recent Garmin data
- Call AnalysisAgent
- Run evaluators
- Log to Opik
- Save to CoachingSession table
- Return recovery assessment

**POST /api/coach/generate-weekly-plan:**
- Get user profile
- Fetch recent workouts and recovery data
- Call PlanningAgent
- Evaluate plan for safety and balance
- Save to WeeklyPlan and Workout tables
- Log to Opik
- Return weekly plan

**POST /api/coach/adapt-today:**
- Get today's scheduled workout
- Fetch today's Garmin data
- Call AdaptationAgent
- Evaluate safety
- Update workout if adapted
- Log to Opik
- Return adapted workout

**POST /api/coach/chat:**
- Accept free-form user message
- Determine intent (use simple classification or LLM)
- Route to appropriate agent
- Evaluate response
- Log to Opik
- Return chat response

**GET /api/coach/insights:**
- Fetch historical data (30-90 days)
- Call InsightsAgent
- Return list of insights

**GET /api/coach/history:**
- Fetch coaching session history
- Include evaluation scores
- Return paginated results

### Step 7.2: Analytics Endpoints

**backend/app/api/analytics.py:**

**GET /api/analytics/recovery-trends:**
- Query GarminData for date range
- Calculate averages and trends
- Return time series data for charts

**GET /api/analytics/workout-adherence:**
- Compare scheduled vs completed workouts
- Calculate adherence percentage
- Return adherence trends

**GET /api/analytics/body-composition:**
- Query body comp data
- Calculate changes over time
- Return trends

**GET /api/analytics/performance:**
- Track running pace improvements
- Track strength progression (weight increases)
- Return performance metrics

---

## PHASE 8: Frontend Development

### Step 8.1: API Service Layer

**frontend/src/services/api.ts:**

Create API client with:
- Axios instance with base URL
- Request interceptor (add auth token)
- Response interceptor (handle errors, refresh tokens)
- Methods for all backend endpoints:
  - auth (login, register, getMe)
  - garmin (connect, sync, status, disconnect)
  - coach (analyzeRecovery, generatePlan, adaptToday, chat, getInsights)
  - analytics (getRecoveryTrends, getAdherence, getBodyComp, getPerformance)

### Step 8.2: Type Definitions

**frontend/src/types/index.ts:**

Define TypeScript interfaces for:
- User, UserProfile
- GarminData, GarminActivity
- Workout, WeeklyPlan
- CoachingSession
- RecoveryStatus
- BodyComposition
- API responses

### Step 8.3: Component Implementation

**1. Dashboard.tsx (Main landing page):**
- Recovery status card (Body Battery gauge, sleep score, stress)
- Today's workout card (show adapted workout if applicable)
- Weekly plan overview (calendar with workout types)
- Body composition trends (line chart)
- Quick actions (sync Garmin, chat with coach, view insights)
- Use Recharts for visualizations
- Real-time updates when data syncs

**2. GarminConnect.tsx:**
- If not connected: Show "Connect Garmin" button → opens OAuth flow
- If connected: Show connection status, last sync time, sync button
- Display sync progress during manual sync
- Handle OAuth callback redirect
- Error handling for auth failures

**3. RecoveryStatus.tsx:**
- Large gauge charts for Body Battery, sleep score, stress
- 7-day trend line charts
- Color coding (red/yellow/green based on thresholds)
- Today's recommendation (rest/light/moderate/hard)
- Detailed metrics breakdown (RHR, HRV, sleep stages)

**4. WorkoutPlan.tsx:**
- Weekly calendar view
- Click day to see workout details
- Exercise list with sets/reps/weight
- Mark workout as complete
- View adaptation explanation if workout was modified
- Previous workout comparison

**5. BodyComposition.tsx:**
- Weight trend chart (30-90 days)
- Body fat percentage trend
- Muscle mass trend
- Monthly snapshots table
- Progress indicators (up/down arrows)

**6. CoachChat.tsx:**
- Chat interface (messages list + input)
- Display user messages and coach responses
- Show "coach is thinking" animation
- Option to view agent reasoning
- Conversation history

**7. OpikDashboard.tsx (For judge demo):**
- Evaluation scores overview (all 7 dimensions)
- Score trends over time (line charts)
- Recent regression test results (pass/fail indicators)
- Experiment comparison table
- Model performance metrics
- Link to full Opik workspace

**8. Navigation Component:**
- Top nav bar with logo, user menu
- Side nav with Dashboard, Workouts, Recovery, Body Comp, Insights, Chat, Opik
- Mobile responsive

### Step 8.4: Routing

**frontend/src/App.tsx:**

Set up React Router with routes:
- / → Dashboard
- /garmin → GarminConnect
- /workouts → WorkoutPlan
- /recovery → RecoveryStatus
- /body-composition → BodyComposition
- /chat → CoachChat
- /opik → OpikDashboard (for demo)
- /login → Login
- /register → Register

Protected routes require authentication.

### Step 8.5: State Management

Use React Context or Zustand for:
- User authentication state
- Garmin connection status
- Current workout plan
- Recovery data
- Notification system

---

## PHASE 9: Opik Experiments & Optimization (DEMO HIGHLIGHT)

### Experiment 1: Data Inclusion Strategy

**Objective:** Determine optimal Garmin data to include in prompts

**Setup:**
1. Create 3 variants in Opik:
   - Variant A: Minimal (today's BB + sleep only)
   - Variant B: Moderate (today + 3-day averages)
   - Variant C: Comprehensive (all metrics + 7-day trends)

2. Randomly assign coaching sessions to variants

3. Track metrics:
   - Evaluation scores (all 7 dimensions)
   - Response latency
   - Token usage (cost proxy)
   - User satisfaction (if collecting feedback)

4. Collect 100+ samples per variant

5. Analyze in Opik:
   - Compare mean scores
   - Statistical significance tests
   - Cost-benefit analysis

**Expected Outcome:**
Comprehensive likely wins on quality but costs more. Choose based on weighted priorities (quality 70%, cost 20%, latency 10%).

**Documentation:**
- Screenshot Opik experiment dashboard
- Write up findings in OPIK_SHOWCASE.md
- Highlight improvement metrics

### Experiment 2: Recovery Algorithm Testing

**Objective:** Test different recovery calculation methods

**Variants:**
- Variant A: Body Battery threshold only (BB <30 = rest)
- Variant B: Weighted formula (0.6 * sleep_score + 0.4 * body_battery)
- Variant C: Multi-factor (BB + sleep + stress + RHR delta)
- Variant D: ML-based (train simple model on historical data)

**Metrics:**
- Recovery assessment accuracy score
- User adherence to recommendations
- Overtraining incident rate
- Performance improvements

**Implementation:**
Run for 2 weeks, collect data, analyze in Opik.

### Experiment 3: Prompt Optimization with Agent Optimizer

**Objective:** Use Opik Agent Optimizer to improve prompts

**Process:**
1. Select agent to optimize (start with AnalysisAgent)
2. Define target metrics (recovery assessment >0.9, safety 1.0, personalization >0.85)
3. Provide current prompt template
4. Provide test scenarios (20+ cases)
5. Run Opik Agent Optimizer (10-20 iterations)
6. Evaluate best prompt on holdout set
7. Deploy to production if improvement >5%

**Focus Areas:**
- Clearer instructions
- Better examples
- Improved reasoning structure
- Safety emphasis

**Documentation:**
- Before/after prompt comparison
- Score improvements (e.g., "73% → 89% personalization")
- Deployment decision rationale

---

## PHASE 10: Testing & Quality Assurance

### Step 10.1: Unit Tests

**backend/tests/test_garmin.py:**
- Test OAuth URL generation
- Test token exchange (mocked)
- Test data parsing functions
- Test error handling

**backend/tests/test_agents.py:**
- Test each agent's prompt building
- Test response parsing
- Mock Anthropic API calls
- Verify Opik logging

**backend/tests/test_evaluations.py:**
- Test each evaluator with known inputs
- Verify scoring logic
- Test edge cases

Run with: `pytest backend/tests/ -v`

### Step 10.2: Integration Tests

Test complete workflows:
1. User registers → connects Garmin → syncs data → gets recovery analysis
2. User requests plan → receives personalized weekly plan → plan passes safety checks
3. Poor recovery detected → workout adapted → adaptation logged and evaluated

### Step 10.3: Regression Testing

**Automated Daily Tests:**
- Run all test scenarios through evaluators
- Log results to Opik
- Alert if any scenario drops below threshold
- Generate test report

**Before Deployment Checklist:**
- All regression tests passing (>95%)
- No evaluation score regressions >5%
- Manual smoke test of critical paths

---

## PHASE 11: Demo Preparation (CRITICAL FOR WINNING)

### Step 11.1: Create Demo User Account

Set up demo@fitsense.ai with:
- Realistic Garmin data:
  - Days 1-3: Good recovery (BB 75+, sleep 85+)
  - Days 4-5: Poor recovery (BB 30, sleep 60, stress 80) → should trigger adaptation
  - Days 6-7: Improving recovery
  - Mix of running and strength workouts
  - Body comp showing progress (weight -2kg, BF% -1.5%)
- Completed workouts showing adherence
- Generated weekly plan
- Chat history with coach
- Insights showing patterns

### Step 11.2: Prepare Demo Script

**5-Minute Live Demo Flow:**

**Minute 1: Hook & Problem (30 seconds)**
- "Generic fitness apps give everyone the same plan"
- "Real problem: Your body's recovery varies daily"
- "Solution: AI coach that adapts based on YOUR Garmin data"

**Minute 2: Core Features (60 seconds)**
- Show dashboard with real Garmin data
- Point out Body Battery (35), poor sleep (62), high stress (78)
- "Today was supposed to be high-intensity intervals..."
- Show adaptation: "Coach changed it to easy recovery run"
- Click to see reasoning: "Low Body Battery + poor sleep = injury risk"

**Minute 3: Weekly Planning (45 seconds)**
- Show weekly plan interface
- Highlight personalization: "Based on your goal: sub-45min 10K"
- Show specific paces: "Tempo runs at 4:35/km (based on recent data)"
- Show progression: "Volume increased 8% from last week (safe range)"

**Minute 4: Opik Evaluation Showcase (90 seconds) - CRITICAL**
- Switch to Opik dashboard
- "This is why FitSense is safe and effective..."
- Show evaluation scores:
  - Safety: 100% (highlight this)
  - Recovery assessment: 91% accuracy
  - Personalization: 89%
- Show experiment results: "We tested 3 data strategies - comprehensive won"
- Show before/after optimization: "Improved personalization from 73% to 89%"
- Show regression tests: "147 scenarios, 98% passing"
- Key message: "Opik ensures our AI gets better, not worse"

**Minute 5: Impact & Future (45 seconds)**
- Body comp progress chart: "User lost 2kg, 1.5% body fat in 6 weeks"
- Safety emphasis: "Zero overtraining incidents in testing"
- "Real users already seeing results"
- Future: "Nutrition coaching, injury rehab, community features"
- Call to action: "Available on GitHub, connect your Garmin today"

### Step 11.3: Backup Materials

Prepare in case live demo fails:
- Video recording of full demo (3 minutes)
- Screenshots of each key screen
- GIF of adaptation in action
- PDF of Opik dashboard
- Architecture diagram

### Step 11.4: Documentation for Judges

**README.md:**
Include:
- Project description and motivation
- Key features with screenshots
- Architecture diagram
- Tech stack
- Setup instructions (Docker Compose one-liner)
- Demo credentials
- Team information
- Links to Opik workspace

**OPIK_SHOWCASE.md:**
Dedicated document highlighting:
- Why Opik integration is exceptional
- All 7 evaluation dimensions with examples
- Experiment comparisons with data tables
- Regression test suite description
- Improvement story with specific metrics
- Screenshots of Opik dashboards
- How Opik influenced development decisions

**ARCHITECTURE.md:**
- System architecture diagram
- Data flow diagrams
- Agent interaction flowchart
- Evaluation pipeline diagram

**DEMO_SCRIPT.md:**
- Full demo script
- Timing guide
- Key talking points
- Judge criteria mapping

---

## PHASE 12: Deployment

### Step 12.1: Local Development

Ensure docker-compose works:
```bash
cp backend/.env.example backend/.env
# Edit .env with real API keys
docker-compose up --build
```

Visit:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

### Step 12.2: Cloud Deployment (Optional)

For hackathon demo:
- **Backend**: Deploy to Railway.app or Render.com
- **Frontend**: Deploy to Vercel or Netlify
- **Database**: Use Neon or Supabase (free tier)
- **Environment**: Set all env vars in platform
- **Custom domain**: Optional but professional

Deployment checklist:
- Set ENVIRONMENT=production
- Set DEBUG=False
- Use strong SECRET_KEY
- Configure CORS for frontend domain
- Set up database backups
- Monitor with Opik

### Step 12.3: Security Checklist

- [ ] All secrets in environment variables
- [ ] No API keys in code or git
- [ ] HTTPS enforced in production
- [ ] CORS configured properly
- [ ] Input validation on all endpoints
- [ ] Rate limiting on expensive endpoints
- [ ] SQL injection prevention (using SQLAlchemy ORM)
- [ ] Password hashing (bcrypt)

---

## PHASE 13: Final Hackathon Checklist

### Submission Requirements:
- [ ] Project title registered: "FitSense AI - Your Adaptive Fitness Coach"
- [ ] Description submitted (use 250-word version)
- [ ] Project image uploaded
- [ ] Team member info complete
- [ ] GitHub repo public
- [ ] README.md comprehensive
- [ ] Demo video uploaded (if required)
- [ ] Live demo accessible

### Code Quality:
- [ ] All core features working
- [ ] No critical bugs
- [ ] Error handling implemented
- [ ] Loading states in UI
- [ ] Mobile responsive (bonus)
- [ ] Comments where needed
- [ ] Clean git history

### Opik Integration (Best Use of Opik - $5K):
- [ ] Multi-agent system fully instrumented
- [ ] 7+ evaluation dimensions implemented
- [ ] All evaluators tested and working
- [ ] Test scenario library (50+ cases)
- [ ] Automated regression tests running
- [ ] 3 experiments completed with results
- [ ] Opik dashboard prepared for demo
- [ ] OPIK_SHOWCASE.md written
- [ ] Clear improvement story documented
- [ ] Before/after metrics compiled

### Garmin Integration (Health & Wellness - $5K):
- [ ] OAuth flow working end-to-end
- [ ] Data sync functional (daily summary, activities, body comp)
- [ ] All Garmin metrics displayed correctly
- [ ] Recovery-based adaptation demonstrated
- [ ] Safety guardrails active
- [ ] Real-world data in demo account

### Demo Preparation:
- [ ] Demo script rehearsed (5-minute version)
- [ ] Demo account loaded with data
- [ ] All features tested in demo flow
- [ ] Backup video recorded
- [ ] Screenshots captured
- [ ] Opik dashboard polished
- [ ] Talking points for each judging criterion
- [ ] Team members know their parts

### Documentation:
- [ ] README.md complete with setup instructions
- [ ] OPIK_SHOWCASE.md highlights integration
- [ ] ARCHITECTURE.md shows system design
- [ ] DEMO_SCRIPT.md ready for reference
- [ ] API documentation (FastAPI auto-docs)
- [ ] Code comments where complex
- [ ] License file (MIT recommended)

---

## Development Timeline (21 Days)

### Week 1: Foundation (Days 1-7)

**Day 1:**
- Project setup (repos, Docker, database)
- Database models
- Authentication system

**Day 2:**
- Garmin OAuth implementation
- Initial data sync logic
- Test with real Garmin account

**Day 3:**
- Complete Garmin integration
- Data parsing and storage
- Garmin API endpoints

**Day 4:**
- Base agent class with Opik
- AnalysisAgent implementation
- First evaluation tests

**Day 5:**
- PlanningAgent implementation
- AdaptationAgent implementation
- Agent orchestration

**Day 6:**
- InsightsAgent implementation
- Coach API endpoints
- End-to-end agent testing

**Day 7:**
- Bug fixes from Week 1
- Integration testing
- Prepare for Week 2

### Week 2: Evaluation & Intelligence (Days 8-14)

**Day 8:**
- All 7 evaluators implementation
- LLM-as-judge prompts

**Day 9:**
- Test scenario library creation
- Regression test framework
- Automated testing setup

**Day 10:**
- Opik service implementation
- Experiment 1 setup (data inclusion)
- Start collecting experiment data

**Day 11:**
- Experiment 2 setup (recovery algorithms)
- Continue data collection
- Analysis of early results

**Day 12:**
- Experiment 3 (prompt optimization with Agent Optimizer)
- Run optimization loop
- Document improvements

**Day 13:**
- Frontend setup (React, TypeScript, Tailwind)
- Dashboard component
- GarminConnect component

**Day 14:**
- RecoveryStatus component
- WorkoutPlan component
- API service layer
- Connect frontend to backend

### Week 3: Polish & Demo (Days 15-21)

**Day 15:**
- BodyComposition component
- CoachChat component
- OpikDashboard component (for judges)

**Day 16:**
- Frontend polish (responsive, loading states, error handling)
- UI/UX improvements
- Mobile testing

**Day 17:**
- Create demo user account
- Load realistic Garmin data
- Generate demo content

**Day 18:**
- Demo script writing
- Rehearse demo flow
- Record backup video
- Screenshot capture

**Day 19:**
- Documentation day
- README.md
- OPIK_SHOWCASE.md
- ARCHITECTURE.md
- Code cleanup

**Day 20:**
- Final testing
- Bug fixes
- Deployment (if cloud hosting)
- Performance optimization

**Day 21:**
- Final demo rehearsal
- Submission preparation
- Video upload
- Team prep for presentation

---

## Judging Criteria Mapping

### Best Use of Opik Prize

**Functionality (Does it work?):**
- ✅ Multi-agent system operational
- ✅ Evaluation pipeline running
- ✅ Experiments completed
- ✅ Regression tests automated
- ✅ Dashboards displaying data

**Real-world relevance:**
- ✅ Solves actual problem (unsafe, generic fitness plans)
- ✅ Health/safety critical application (injuries are real)
- ✅ Opik ensures reliability in production

**Use of LLMs/Agents:**
- ✅ 5 specialized agents with clear roles
- ✅ Complex reasoning (recovery analysis, adaptation logic)
- ✅ Tool use (Garmin API, data analysis)
- ✅ Multi-turn conversations
- ✅ Retrieval for exercise library

**Evaluation and observability:**
- ✅✅✅ 7+ evaluation dimensions
- ✅✅✅ LLM-as-judge implementation
- ✅✅✅ Comprehensive test scenario library
- ✅✅✅ Automated regression testing
- ✅✅✅ Safety guardrails with metrics
- ✅✅✅ Continuous improvement loop

**Goal Alignment (Opik):**
- ✅✅✅ Opik integrated from day 1
- ✅✅✅ Used for development decisions (experiments)
- ✅✅✅ Clear improvement story (73% → 89%)
- ✅✅✅ Meaningful insights produced
- ✅✅✅ Dashboards clearly presented

### Health, Fitness & Wellness Prize

**Functionality:**
- ✅ Garmin sync working
- ✅ Workouts generated
- ✅ Adaptation based on recovery
- ✅ Body composition tracking
- ✅ All features stable

**Real-world relevance:**
- ✅✅ Addresses real pain point
- ✅✅ Zero-friction (auto Garmin sync)
- ✅✅ Fits into actual lives
- ✅✅ Sustainable approach

**Use of LLMs/Agents:**
- ✅ Sophisticated multi-agent system
- ✅ Context-aware reasoning
- ✅ Personalized recommendations

**Evaluation and observability:**
- ✅ Comprehensive Opik integration
- ✅ Safety monitoring
- ✅ Quality assurance

**Goal Alignment (Health):**
- ✅✅ Supports fitness goals (strength, endurance, body comp)
- ✅✅ Promotes sustainable habits
- ✅✅ Recovery-focused (prevents burnout)

**Safety and responsibility:**
- ✅✅✅ Safety evaluator (100% score requirement)
- ✅✅✅ Medical disclaimers present
- ✅✅✅ Conservative recommendations
- ✅✅✅ Evidence-based approach
- ✅✅✅ Injury prevention focus

---

## Key Differentiation Points

### vs. Generic Fitness Apps:
- ❌ They: Static plans for everyone
- ✅ FitSense: Personalized daily adaptation

- ❌ They: Manual workout logging
- ✅ FitSense: Automatic Garmin sync

- ❌ They: Ignore recovery state
- ✅ FitSense: Recovery-driven programming

### vs. Other AI Fitness Apps:
- ❌ They: Generic AI coaching
- ✅ FitSense: Specialized multi-agent system

- ❌ They: No quality assurance
- ✅ FitSense: Comprehensive Opik evaluation

- ❌ They: Unproven safety
- ✅ FitSense: Safety-first with metrics

### vs. Human Coaches:
- ❌ Human: Expensive ($100-300/month)
- ✅ FitSense: Accessible

- ❌ Human: Limited availability
- ✅ FitSense: 24/7 access

- ✅ Human: Expertise and personalization
- ✅ FitSense: Data-driven + expert knowledge

---

## Post-Hackathon Roadmap

### If You Win:

**Immediate (Week 1-2):**
- User feedback collection
- Bug fixes from demo
- Documentation expansion
- Social media announcement

**Short-term (Month 1-3):**
- Beta testing with 20-50 real users
- Collect real usage data
- Refine agents based on feedback
- Add Apple Health integration
- Build iOS/Android apps

**Medium-term (Month 4-6):**
- Nutrition coaching module
- Injury prevention protocols
- Community features
- Coach marketplace (connect with human coaches)
- Subscription model exploration

**Long-term (Month 7-12):**
- Professional coach dashboard (manage multiple clients)
- Integration with gym equipment
- Corporate wellness partnerships
- Research partnerships (validate effectiveness)
- Scale infrastructure

### Monetization Options:
- Freemium (basic free, advanced features $10/month)
- Coach partnerships (revenue share)
- Corporate wellness (B2B)
- White-label for gyms/trainers
- API access for developers

---

## Conclusion

This guide provides everything needed to build a winning hackathon project that:

1. **Solves a real problem**: Generic fitness plans don't adapt to individual recovery
2. **Uses cutting-edge tech**: Multi-agent LLMs with comprehensive evaluation
3. **Delivers real value**: Safer, more effective training
4. **Showcases Opik exceptionally**: 7+ evaluations, experiments, continuous improvement
5. **Demonstrates health impact**: Recovery-based programming prevents injury

**Success Formula:**
- Working demo > Perfect code
- Clear story > Technical complexity
- User value > Feature count
- Safety focus > Aggressive recommendations
- Opik integration > Afterthought

**Final Reminder:**
You're building a tool that could genuinely help people train smarter, recover better, and avoid injuries. The judges will feel that authenticity if you build with users in mind.

Good luck! 🚀💪