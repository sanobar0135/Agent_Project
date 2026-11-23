from research.research_agent import run_research_agent
from research.coverage_evaluator import evaluate_research_coverage
from research.findings_cleanup import clean_papers

def _short_query(subtopic, missing):
    # Keep API queries short: the subtopic plus a compact phrase from gap feedback.
    missing = str(missing or "").replace(",", " ").replace(";", " ")
    words = missing.split()
    return (subtopic + " " + " ".join(words[:8])).strip()

def run_additional_research(all_findings, max_rounds=2, threshold=7):
    round_number = 0
    previous_total = sum(len(f.get("papers", [])) for f in all_findings)
    while round_number < max_rounds:
        print("\n========== SUPERVISOR COVERAGE CHECK ==========")
        evaluations = evaluate_research_coverage(all_findings)
        gaps = [e for e in evaluations if e.get("needs_more_research", False) or e.get("score", 0) < threshold]
        if not gaps:
            print("All research tasks have acceptable coverage. Stopping.")
            break
        round_number += 1
        print(f"Additional Research Round {round_number}; gaps: {len(gaps)}")
        for gap in gaps:
            subtopic = gap["subtopic"]
            missing = gap.get("missing_areas", "")
            original = next((f for f in all_findings if f["subtopic"] == subtopic), None)
            if not original: continue
            task = {
                "subtopic": subtopic,
                "objective": f"Investigate gaps: {missing}",
                "search_query": _short_query(subtopic, missing)
            }
            new = run_research_agent(task, max_results=3)
            if new.get("search_failed"):
                print(f"Skipping merge for failed search: {subtopic}")
                continue
            original["papers"] = clean_papers(original.get("papers", []) + new.get("papers", []))
            original["papers_found"] = len(original["papers"])
        total = sum(len(f.get("papers", [])) for f in all_findings)
        if total <= previous_total:
            print("No new papers were added this round; stopping to avoid repeated searches.")
            break
        previous_total = total
    print(f"Additional research rounds: {round_number}")
    return all_findings
