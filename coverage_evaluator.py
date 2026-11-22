
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_research_coverage(all_findings):

    if not all_findings:
        return []

    research_context = []

    for finding in all_findings:

        papers = []

        for paper in finding.get("papers", []):

            papers.append({
                "title": paper.get("title", ""),
                "abstract": paper.get("abstract", ""),
                "year": paper.get("year", "")
            })

        research_context.append({
            "subtopic": finding.get("subtopic", ""),
            "objective": finding.get("objective", ""),
            "papers": papers
        })

    prompt = f"""
    You are an academic research supervisor.

    Evaluate how well each research task has been covered
    by the retrieved research papers.

    Evaluate the papers based on their titles and abstracts.

    For every task:

    1. Give a coverage score from 1 to 10.
    2. Explain your score briefly.
    3. Identify what is still missing.
    4. Decide whether more research is needed.

    Scoring:
    1-3: Very poor coverage
    4-6: Partial coverage
    7-8: Good coverage
    9-10: Strong coverage

    A task should not receive a high score merely because
    papers were found. Evaluate their relevance to the task.

    Return ONLY valid JSON in this format:

    {{
        "evaluations": [
            {{
                "subtopic": "Research subtopic",
                "score": 8,
                "reason": "Explanation",
                "missing_areas": "What is missing",
                "needs_more_research": false
            }}
        ]
    }}

    Research findings:

    {json.dumps(research_context, ensure_ascii=False)}
    """

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    result = json.loads(content)

    evaluations = result["evaluations"]

    print("\n========== COVERAGE EVALUATION ==========")

    for evaluation in evaluations:

        print("\nSubtopic:", evaluation["subtopic"])
        print("Coverage score:", evaluation["score"], "/ 10")
        print("Reason:", evaluation["reason"])
        print("Missing areas:", evaluation["missing_areas"])

        if evaluation["needs_more_research"]:
            print("Decision: MORE RESEARCH NEEDED")
        else:
            print("Decision: COVERAGE ACCEPTABLE")

    print("\n========================================")

    return evaluations
