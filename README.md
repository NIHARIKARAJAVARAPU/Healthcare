# AI-First CRM HCP Module

This project is a beginner-friendly starter for **Task 1: AI-First CRM HCP Module - LogInteractionScreen (Technical)**.

It includes:

- `frontend/`: React UI with Redux for structured form logging and AI chat logging
- `backend/`: FastAPI app with LangGraph agent design and Groq model integration
- `docs/`: architecture notes, tool definitions, and setup walkthrough
- `docker-compose.yml`: one-command PostgreSQL startup for beginners

## 1. What this project does

The screen allows a life-science field representative to log an interaction with an HCP in two ways:

- **Structured form**: direct entry of HCP name, interaction type, date/time, topics, materials, samples, sentiment, outcomes, and follow-up
- **Conversational chat**: the rep types a natural language summary such as:

`Today I met with Dr. Smith and discussed Product X efficacy. The sentiment was positive, and I shared brochures.`

The AI assistant uses **LangGraph + Groq** to:

- extract structured fields
- suggest follow-up actions
- flag compliance-sensitive terms
- support editing of a draft interaction

## 2. Recommended architecture

- Frontend: React + Redux Toolkit + Vite
- Backend: Python + FastAPI + SQLAlchemy
- AI agent: LangGraph + Groq `gemma2-9b-it`
- Optional larger-context model: Groq `llama-3.3-70b-versatile`
- Database: PostgreSQL recommended

## 3. Folder structure

```text
AI-First-CRM-HCP-Module/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/interactions/
│   │   └── styles/
│   └── package.json
├── docs/
└── README.md
```

## 4. Step-by-step: from folder creation to execution

### Step 1: Create the project folder

If you want to recreate it manually:

```powershell
mkdir AI-First-CRM-HCP-Module
cd AI-First-CRM-HCP-Module
mkdir backend, frontend, docs
```

### Step 2: Backend setup

Go to the backend folder:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env`:

- add your new Groq API key
- keep `GROQ_MODEL=gemma2-9b-it`
- set `DATABASE_URL` to your PostgreSQL or MySQL connection string

### Step 3: Database setup

Recommended: PostgreSQL

Easiest option with Docker:

```powershell
docker compose up -d
```

This starts PostgreSQL with:

- database: `ai_crm_hcp`
- username: `postgres`
- password: `postgres`

Manual option:

Create a database named `ai_crm_hcp`.

Example:

```sql
CREATE DATABASE ai_crm_hcp;
```

Then run the backend:

```powershell
uvicorn app.main:app --reload
```

The API will start at:

`http://localhost:8000`

Health check:

`http://localhost:8000/health`

### Step 4: Frontend setup

Open a new terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will start at:

`http://localhost:5173`

## 5. Main APIs

- `POST /api/v1/interactions`: save a structured interaction
- `PUT /api/v1/interactions/{id}`: edit an existing interaction
- `GET /api/v1/interactions`: list interactions
- `POST /api/v1/agent/chat`: send chat text to the LangGraph assistant

## 6. Important note

In this environment, I could scaffold the project files, but I could not fully run the frontend because `node`/`npm` are not available here. The backend dependencies also require package installation, which depends on your local setup and Groq credentials.

For the most beginner-friendly walkthrough, use:

[docs/run-guide.md](C:\Users\NIHARIKA\Documents\Codex\2026-04-23-files-mentioned-by-the-user-instructions\docs\run-guide.md)

## 7. Submission help

If you want, the next step I can do is:

1. prepare a **presentation-ready explanation** for this assignment
2. add **PostgreSQL Docker setup**
3. add **screenshots / demo script**
4. make the UI even closer to your reference images


