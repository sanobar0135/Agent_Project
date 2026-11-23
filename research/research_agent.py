from research.paper_search import search_papers
from research.findings_cleanup import clean_papers

def run_research_agent(task, max_results=3):
    subtopic, objective = task["subtopic"], task.get("objective", "")
    query = task.get("search_query", subtopic)
    print(f"\nStarting Research Agent: {subtopic}\nSearch query: {query}")
    try:
        papers = clean_papers(search_papers(query, max_results=max_results))
        failed, error_text = False, None
    except Exception as error:
        print("Research search failed:", error)
        papers, failed, error_text = [], True, str(error)
    return {"subtopic": subtopic, "objective": objective, "papers_found": len(papers),
            "papers": papers, "search_failed": failed, "search_error": error_text}
