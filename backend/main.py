import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import research_routes
app=FastAPI(title="Deep Research Agent API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(research_routes.router,prefix="/api")
@app.get("/api/health")
def health(): return {"status":"ok"}
