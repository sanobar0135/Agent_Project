from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.services.research_service import start_research, get_run, list_runs, get_report
router=APIRouter()
class ResearchRequest(BaseModel):
    topic: str = Field(min_length=5,max_length=500)
@router.post("/research")
def create(req:ResearchRequest):
    return start_research(req.topic.strip())
@router.get("/research/{run_id}")
def status(run_id:str):
    data=get_run(run_id)
    if not data: raise HTTPException(404,"Research run not found")
    return data
@router.get("/history")
def history(): return list_runs()
@router.get("/research/{run_id}/report")
def report(run_id:str):
    r=get_report(run_id)
    if not r: raise HTTPException(404,"Report is not ready")
    return {"report":r}
