# Deep Research Agent — Existing project enhanced

This is an extension of the original Python CLI project. Existing research modules are retained and used by the FastAPI backend.

## Backend setup (project root)
1. Activate the project's existing virtual environment.
2. Install: `pip install -r requirements.txt`
3. Ensure the existing `.env` contains `GROQ_API_KEY` and optionally `GROQ_MODEL`.
4. Run: `uvicorn backend.main:app --reload`
5. API docs: http://127.0.0.1:8000/docs

## Frontend
In another terminal:
`cd frontend`
`npm install`
`npm run dev`
Open http://localhost:5173.

## API
- GET `/api/health`
- POST `/api/research` JSON `{"topic":"..."}`
- GET `/api/research/{run_id}`
- GET `/api/research/{run_id}/report`
- GET `/api/history`

## CLI remains available
Run `python3 app.py` to use the original CLI.

SQLite research history is stored in `research_history.db` at the project root.
