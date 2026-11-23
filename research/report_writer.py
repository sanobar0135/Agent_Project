def generate_report(topic, papers):
    """
    Generate a basic literature review report
    from the collected research papers.
    """

    report = []

    report.append("# Literature Review")
    report.append(f"\n## Topic: {topic}")
    report.append("\n## Introduction")
    report.append(
        f"\nThis report reviews research papers related to {topic}. "
        "It organizes the collected research to explore relevant "
        "approaches, findings and limitations."
    )

    report.append("\n## Research Papers")

    for i, paper in enumerate(papers, start=1):

        report.append(f"\n### {i}. {paper['title']}")
        report.append(f"\n**Year:** {paper.get('year', 'Unknown')}")

        report.append(
            f"\n**Authors:** {', '.join(paper.get('authors', []))}"
        )

        report.append("\n**Abstract:**")
        report.append(paper.get("abstract", "No abstract available"))

        report.append(
            f"\n**Source:** {paper.get('source', 'Unknown')}"
        )

        report.append(
            f"\n**Link:** {paper.get('url', 'No link available')}"
        )

    report.append("\n## Conclusion")
    report.append(
        "\nThe collected papers provide an overview of the research "
        f"available on {topic}. Further analysis can compare methods, "
        "identify common limitations and highlight future research directions."
    )

    return "\n".join(report)


def save_report(report, filename="literature_review.md"):
    """
    Save the report as a Markdown file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved successfully: {filename}")