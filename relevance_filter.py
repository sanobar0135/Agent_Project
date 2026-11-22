import json

from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def filter_relevant_papers(topic, papers, threshold=7):

    if not papers:
        return []

    paper_context = []

    for i, paper in enumerate(papers, start=1):

        paper_context.append({
            "id": i,
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", "")
        })

    prompt = f"""
    You are an academic research relevance evaluator.

    Main research topic:
    {topic}

    Evaluate the relevance of each paper to the main research topic.

    Score each paper from 1 to 10.

    Scoring guidelines:
    1-3: Unrelated
    4-6: Partially related
    7-8: Relevant
    9-10: Highly relevant

    Evaluate based on the title and abstract.

    Do not assume information that is not provided.

    Return ONLY valid JSON in this format:

    {{
        "evaluations": [
            {{
                "id": 1,
                "score": 8,
                "reason": "Short explanation"
            }}
        ]
    }}

    Papers:
    {json.dumps(paper_context, ensure_ascii=False)}
    """

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    result = json.loads(content)

    evaluations = result["evaluations"]

    evaluation_map = {
        item["id"]: item
        for item in evaluations
    }

    relevant_papers = []

    print("\n========== PAPER RELEVANCE CHECK ==========")

    for i, paper in enumerate(papers, start=1):

        evaluation = evaluation_map.get(i)

        if not evaluation:
            continue

        score = evaluation["score"]
        reason = evaluation["reason"]

        print("\nPaper:", paper["title"])
        print("Relevance score:", score)
        print("Reason:", reason)

        if score >= threshold:

            relevant_papers.append(paper)

            print("Status: ACCEPTED")

        else:

            print("Status: REJECTED")

    print("\nPapers before filtering:", len(papers))
    print("Papers after filtering:", len(relevant_papers))
    print("==========================================")

    return relevant_papers