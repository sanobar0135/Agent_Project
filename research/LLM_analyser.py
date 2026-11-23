import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MAX_PAPERS = 4
MAX_ABSTRACT_LENGTH = 500
MAX_OUTPUT_TOKENS = 1500


def analyze_research(topic, papers):

    selected_papers = papers[:MAX_PAPERS]

    paper_context = []

    for i, paper in enumerate(selected_papers, start=1):

        abstract = paper.get("abstract", "") or ""
        abstract = abstract[:MAX_ABSTRACT_LENGTH]

        paper_context.append(
            f"Paper {i}: {paper.get('title', '')}\n"
            f"Authors: {paper.get('authors', [])}\n"
            f"Year: {paper.get('year', '')}\n"
            f"Abstract: {abstract}\n"
        )

    paper_context = "\n".join(paper_context)

    prompt = f"""
Research topic: {topic}

Analyze these academic papers using ONLY their provided information.
Do not invent findings, authors, citations or results.
Cite papers using their titles.

Write a concise but informative literature review with:

1. Topic overview
2. Major methods and techniques
3. Common themes
4. Method differences
5. Reported limitations
6. Potential research gaps
7. Conclusion

Clearly separate reported limitations from inferred research gaps.
Use Markdown headings and concise paragraphs.
Use tables only when they improve clarity.

Papers:

{paper_context}
"""

    try:

        response = client.chat.completions.create(
            model=os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-120b"
            ),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=MAX_OUTPUT_TOKENS
        )

        report = response.choices[0].message.content or ""

        # Append references directly from source records
        references = "\n\n## References / Papers Reviewed\n\n"

        for i, paper in enumerate(selected_papers, start=1):

            title = paper.get("title", "Untitled paper")
            url = paper.get("url", "")
            authors = paper.get("authors", [])
            year = paper.get("year", "")

            if isinstance(authors, list):
                authors = ", ".join(authors[:3])
                if len(paper.get("authors", [])) > 3:
                    authors += " et al."

            references += f"{i}. **{title}**"

            if authors:
                references += f" — {authors}"

            if year:
                references += f" ({year})"

            if url:
                references += f"\n   - Link: {url}"

            references += "\n\n"

        return report + references

    except Exception as e:

        print(f"Research analysis error: {e}")

        return (
            "LLM synthesis could not be completed because of a "
            "Groq rate or API limitation. The collected research "
            "data is still available. Please retry after a short wait."
        )