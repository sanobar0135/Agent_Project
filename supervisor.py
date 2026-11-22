
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def create_research_tasks(topic):

    prompt = f"""
    You are an academic research supervisor.

    Research topic:
    {topic}

    Break this topic into 4 to 5 meaningful and distinct research areas.

    Each research task should:
    - Focus on a specific aspect of the topic.
    - Avoid overlapping with other tasks.
    - Be suitable for a research paper search.
    - Help build a comprehensive literature review.

    Return ONLY valid JSON in this format:

    {{
        "tasks": [
            {{
                "subtopic": "Research subtopic",
                "objective": "Research objective"
            }}
        ]
    }}
    """

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    result = json.loads(content)

    return result["tasks"]


def print_research_tasks(tasks):

    print("\n========== SUPERVISOR PLAN ==========")

    for i, task in enumerate(tasks, start=1):

        print(f"\nResearch Agent {i}")
        print("Subtopic:", task["subtopic"])
        print("Objective:", task["objective"])

    print("\nTotal research tasks:", len(tasks))
    print("====================================")
