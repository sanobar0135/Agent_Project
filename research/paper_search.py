
import arxiv


def search_papers(topic, max_results=5):
    """
    Search research papers on arXiv.

    Args:
        topic: Research topic or search query.
        max_results: Number of papers to retrieve.

    Returns:
        A list of structured paper information.
    """

    client = arxiv.Client()

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in client.results(search):
        paper = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "year": result.published.year,
            "abstract": result.summary,
            "url": result.entry_id,
            "source": "arxiv"
        }

        papers.append(paper)

    return papers
