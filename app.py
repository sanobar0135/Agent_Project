from relevance_filter import filter_relevant_papers
from scope import generate_research_brief, print_research_brief
from paper_search import search_papers
from findings_cleanup import clean_papers
from supervisor import create_research_tasks, print_research_tasks

from parallel_agents import run_agents_parallel

from research_review import (
    merge_findings,
    check_research_coverage,
    print_research_review
)

from research_loop import run_additional_research
from LLM_analyser import analyze_research
from report_writer import save_report


def main():

    topic = input("Enter your research topic: ")

    print("\nTopic is clear. Skipping clarification.")

    # Step 1: Generate research brief
    brief = generate_research_brief(topic)
    print_research_brief(brief)

    # Step 2: Initial paper search
    print("\nSearching initial research papers...\n")

    papers = search_papers(topic, max_results=5)

    print("Raw papers retrieved:", len(papers))

    cleaned_papers = clean_papers(papers)

    print("Clean papers after cleanup:", len(cleaned_papers))

    # Step 3: Supervisor creates tasks
    tasks = create_research_tasks(topic)

    print_research_tasks(tasks)

    # Step 4: Execute research agents in parallel
    all_findings = run_agents_parallel(
        tasks,
        max_results=3
    )

    # Step 5: Additional research loop
    all_findings = run_additional_research(
        all_findings,
        max_rounds=2
    )

    # Step 6: Merge findings
    merged_papers = merge_findings(all_findings)

    # Step 7: Filter irrelevant papers using LLM
    print("\nFiltering papers by relevance...")

    relevant_papers = filter_relevant_papers(
        topic,
        merged_papers,
        threshold=7
)
    # Step 8: Display research review
    print_research_review(
        all_findings,
        merged_papers,
        gaps=check_research_coverage(all_findings)
    )

    # Step 9: LLM research analysis
    print("\n========== LLM RESEARCH ANALYSIS ==========")

    print("Sending collected papers to LLM...")

    analysis = analyze_research(
        topic,
        relevant_papers
    )

    print("\nAnalysis generated successfully!")

    print(analysis)

    # Step 10: Save report
    print("\nSaving literature review...")

    save_report(
        analysis,
        filename="literature_review.md"
    )

    print("\nResearch project completed successfully!")


if __name__ == "__main__":
    main()