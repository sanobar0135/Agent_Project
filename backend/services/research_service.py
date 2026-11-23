import threading, uuid, time, json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.database.db import init_db, save_run, update_run, fetch_run, fetch_history
init_db()
_jobs={}
def _pipeline(run_id,topic):
    update_run(run_id,status="running",stage="Creating research brief")
    try:
        from research.scope import generate_research_brief
        from research.supervisor import create_research_tasks
        from research.parallel_agents import run_agents_parallel
        from research.research_loop import run_additional_research
        from research.research_review import merge_findings
        from research.relevance_filter import filter_relevant_papers
        from research.LLM_analyser import analyze_research
        brief=generate_research_brief(topic)
        update_run(run_id,stage="Planning research tasks",brief=brief)
        tasks=create_research_tasks(topic)
        update_run(run_id,stage=f"Researching {len(tasks)} subtopics",tasks=tasks)
        findings=run_agents_parallel(tasks,max_results=3)
        update_run(run_id,stage="Evaluating coverage and conducting follow-up research")
        findings=run_additional_research(findings,max_rounds=2)
        papers=merge_findings(findings)
        update_run(run_id,stage="Filtering papers",findings=findings,papers=papers)
        relevant=filter_relevant_papers(topic,papers,threshold=7)
        update_run(run_id,stage="Writing literature review")
        report=analyze_research(topic,relevant)
        update_run(run_id,status="completed",stage="Completed",brief=brief,tasks=tasks,findings=findings,
                   papers=papers,relevant_papers=relevant,report=report,error=None)
    except Exception as e:
        update_run(run_id,status="failed",stage="Failed",error=str(e))
def start_research(topic):
    rid=str(uuid.uuid4())
    save_run(rid,topic)
    _jobs[rid]=threading.Thread(target=_pipeline,args=(rid,topic),daemon=True)
    _jobs[rid].start()
    return {"run_id":rid,"status":"queued"}
def get_run(rid): return fetch_run(rid)
def list_runs(): return fetch_history()
def get_report(rid):
    r=fetch_run(rid)
    return r.get("report") if r and r.get("status")=="completed" else None
