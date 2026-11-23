#This module will prepare the retrieved papers into clean, structured information that our future research agents and report writer can use.


def clean_text(text):
    """Clean unnecessary whitespace from text."""
    if not text:
        return ""

    return " ".join(text.split())


def clean_papers(papers):
    """Clean paper records and remove duplicate papers."""

    cleaned_papers = []
    seen_titles = set()

    for paper in papers:

        # Clean the title
        title = clean_text(paper.get("title", ""))

        # Skip papers without a title
        if not title:
            continue

        # Create a normalized title for duplicate detection
        normalized_title = title.lower()

        # Skip duplicate papers
        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)

        # Clean abstract
        abstract = clean_text(paper.get("abstract", ""))

        # Clean authors
        authors = paper.get("authors", [])

        # Prepare clean paper data
        cleaned_paper = {
            "title": title,
            "authors": authors,
            "year": paper.get("year"),
            "abstract": abstract,
            "url": paper.get("url", ""),
            "source": paper.get("source", "unknown")
        }

        cleaned_papers.append(cleaned_paper)

    return cleaned_papers
