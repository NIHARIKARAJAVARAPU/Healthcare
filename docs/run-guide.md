# Beginner Run Guide

This guide assumes you are on Windows and starting from zero.

## Software to install first

Install these before running the project:

1. Python 3.11 or newer
2. Node.js 20 or newer
3. Docker Desktop
4. VS Code or any code editor

## Step 1: Open the project

Open the folder:

[2026-04-23-files-mentioned-by-the-user-instructions](C:\Users\NIHARIKA\Documents\Codex\2026-04-23-files-mentioned-by-the-user-instructions)

## Step 2: Start PostgreSQL with Docker

Open PowerShell in the project root and run:

```powershell
docker compose up -d
```

This starts PostgreSQL on port `5432`.

## Step 3: Configure backend environment

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

Now open `.env` and replace:

```text
GROQ_API_KEY=your_new_groq_api_key_here
```

with your actual Groq API key.

Keep this model:

```text
GROQ_MODEL=gemma2-9b-it
```

## Step 4: Run backend

Still inside `backend/`, run:

```powershell
uvicorn app.main:app --reload
```

You should see FastAPI running at:

[http://localhost:8000](http://localhost:8000)

Health check:

[http://localhost:8000/health](http://localhost:8000/health)

## Step 5: Run frontend

Open a second PowerShell window:

```powershell
cd C:\Users\NIHARIKA\Documents\Codex\2026-04-23-files-mentioned-by-the-user-instructions\frontend
npm install
npm run dev
```

Open:

[http://localhost:5173](http://localhost:5173)

## Step 6: Test the AI chat flow

Paste a message like:

```text
Today I met with Dr. Smith and discussed Product X efficacy. The sentiment was positive, and I shared brochures.
```

Expected behavior:

1. The assistant replies with a CRM-friendly summary
2. The form auto-populates fields such as HCP name, topic, sentiment, and materials shared
3. You can review and click `Save Interaction`

## Step 7: What to say in your submission/demo

You can explain the project like this:

- The screen supports both manual form entry and AI-assisted conversational logging.
- The backend uses FastAPI and LangGraph.
- Groq `gemma2-9b-it` is used for structured extraction and summarization.
- Redux keeps the chat and form in sync in the frontend.
- PostgreSQL stores interaction records.

## Common problems

### `npm` not recognized

Install Node.js from the official website and reopen PowerShell.

### Database connection error

Make sure Docker Desktop is running and `docker compose up -d` completed successfully.

### Groq auth error

Double-check the `GROQ_API_KEY` value in `backend/.env`.
