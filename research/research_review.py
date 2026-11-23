from research.findings_cleanup import clean_papers


def merge_findings(all_findings):
    """
    Merge paper findings from all research agents
    and remove duplicate papers.
    """

    all_papers = []

    for finding in all_findings:
        all_papers.extend(finding["papers"])

    unique_papers = clean_papers(all_papers)

    return unique_papers


def check_research_coverage(all_findings):
    """
    Check whether each research task returned papers.
    """

    gaps = []

    for finding in all_findings:

        if finding["papers_found"] == 0:

            gaps.append({
                "subtopic": finding["subtopic"],
                "objective": finding["objective"]
            })

    return gaps


def print_research_review(all_findings, merged_papers, gaps):

    print("\n========== RESEARCH REVIEW ==========")

    print("Agents reviewed:", len(all_findings))
    print("Total agent paper records:",
          sum(f["papers_found"] for f in all_findings))

    print("Unique papers after merging:", len(merged_papers))

    if gaps:

        print("\nResearch areas needing more investigation:")

        for gap in gaps:
            print("-", gap["subtopic"])

    else:

        print("\nAll planned research areas returned papers.")

    print("====================================")