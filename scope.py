
def generate_research_brief(topic):
    brief = {
        "topic": topic,
        "objective": f"Study and analyze research related to {topic}.",
        "scope": [
            "Identify important research methods",
            "Study existing approaches",
            "Analyze research findings",
            "Identify limitations and research gaps"
        ],
        "output": "A cited literature review"
    }

    return brief


def print_research_brief(brief):
    print("\n========== RESEARCH BRIEF ==========")

    print("Topic:", brief["topic"])
    print("Objective:", brief["objective"])

    print("\nScope:")

    for item in brief["scope"]:
        print("-", item)

    print("\nExpected Output:", brief["output"])
    print("===================================")
