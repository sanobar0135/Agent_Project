from research.paper_search import search_papers
from research.findings_cleanup import clean_papers
from research.LLM_analyser import analyze_research


topic = "Parameter-efficient fine-tuning methods for LLMs"

print("Searching papers...")

papers = search_papers(topic, max_results=3)

papers = clean_papers(papers)

print("Sending research to LLM...")

analysis = analyze_research(topic, papers)

print("\n========== LLM RESEARCH ANALYSIS ==========\n")

print(analysis)

print("\n==========================================")