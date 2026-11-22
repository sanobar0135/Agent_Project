from concurrent.futures import ThreadPoolExecutor, as_completed
from research_agent import run_research_agent

def run_agents_parallel(tasks, max_results=3):
    findings=[]
    print("\n========== PARALLEL RESEARCH ==========")
    print(f"Starting {len(tasks)} research agents concurrently...")
    with ThreadPoolExecutor(max_workers=max(1, min(len(tasks), 8))) as executor:
        futures={executor.submit(run_research_agent, task, max_results):task for task in tasks}
        for future in as_completed(futures):
            task=futures[future]
            try: item=future.result()
            except Exception as exc:
                item={"subtopic":task["subtopic"],"objective":task.get("objective",""),
                      "papers_found":0,"papers":[],"search_failed":True,"search_error":str(exc)}
            findings.append(item)
            print(f"Completed agent: {task['subtopic']} | papers: {item.get('papers_found',0)}")
    print("All agents have finished.")
    return findings
