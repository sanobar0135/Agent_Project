from research_agent import run_research_agent

sample_task = {
    "subtopic": "LoRA methods for fine-tuning LLMs",
    "objective": "Understand how LoRA reduces trainable parameters."
}

findings = run_research_agent(sample_task, max_results=3)

print("\n========== AGENT FINDINGS ==========")
print("Subtopic:", findings["subtopic"])
print("Objective:", findings["objective"])
print("Papers found:", findings["papers_found"])

for i, paper in enumerate(findings["papers"], start=1):
    print(f"\n--- Paper {i} ---")
    print("Title:", paper["title"])
    print("Year:", paper["year"])
    print("Authors:", paper["authors"])
    print("Abstract:", paper["abstract"])
    print("URL:", paper["url"])

print("====================================")