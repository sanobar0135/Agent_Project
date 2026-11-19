# Deep Research Agent for Research Papers

## About the Project

The **Deep Research Agent** is a student project that aims to make
research-paper exploration easier. Instead of manually searching for
papers, reading them one by one, and organizing the information, the
system uses AI agents to research a topic and prepare a structured
literature review.

The project follows three main phases:

**Scope → Research → Write**

## How It Works

1.  **Scope:** The system understands the user's research topic. If the
    topic is unclear, it may ask a few questions. It then creates a
    focused Research Brief.
2.  **Research:** A Research Supervisor divides the topic into smaller
    tasks and assigns them to research sub-agents. These agents search
    academic sources such as arXiv, Semantic Scholar, or OpenAlex.
3.  **Findings Cleanup:** Research results are organized and summarized
    so that useful findings and paper details are easier to work with.
4.  **Research Gap Check:** The supervisor checks whether the collected
    research covers the brief. If information is missing, it can request
    additional research, with a maximum of two extra rounds.
5.  **Write:** A single AI call combines the brief and collected
    findings into a literature review with citations, a paper comparison
    table, research gaps, and references.

## Main Features

-   Accepts a research topic from the user.
-   Creates a focused Research Brief.
-   Searches academic paper sources.
-   Uses multiple research sub-agents for different subtopics.
-   Supports parallel research.
-   Cleans and summarizes research findings.
-   Checks for research gaps and allows up to two additional rounds.
-   Generates a literature review with citations and references.
-   Includes evaluation using five test topics.

## Project Workflow

``` mermaid
flowchart TD
    A[User enters research topic] --> B[Scope and Research Brief]
    B --> C[Research Supervisor]
    C --> D[Assign subtopics]
    D --> E[Research Sub-agents]
    E --> F[Search academic paper APIs]
    F --> G[Clean findings]
    G --> H[Supervisor checks coverage]
    H --> I{Research sufficient?}
    I -->|No, rounds remain| D
    I -->|Yes or limit reached| J[Report Writer]
    J --> K[Final Literature Review]
```

## Technology Stack

-   **Python:** Main programming language.
-   **LLM API:** Helps understand topics, summarize research, and
    generate reports.
-   **LangGraph / LangChain:** Helps organize the agent workflow.
-   **arXiv API:** Search for research papers.
-   **Semantic Scholar / OpenAlex:** Optional additional paper sources.
-   **Git and GitHub:** Version control and team collaboration.

> The technology stack may change as the project is developed.

## Project Structure

``` text
deep-research-agent/
├── app.py
├── scope.py
├── paper_search.py
├── supervisor.py
├── research_agent.py
├── findings_cleanup.py
├── report_writer.py
├── evaluation.py
├── requirements.txt
├── .env
└── README.md
```

## Getting Started

### 1. Clone the repository

``` bash
git clone <your-github-repository-url>
cd deep-research-agent
```

### 2. Create a virtual environment

``` bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

``` bash
source venv/bin/activate
```

**Windows:**

``` bash
venv\Scripts\activate
```

### 4. Install dependencies

``` bash
pip install -r requirements.txt
```

If the requirements file is not ready yet, install packages as they are
added during development.

### 5. Configure API keys

Create a `.env` file in the project folder and add the API keys required
by the LLM provider you choose.

``` text
LLM_API_KEY=your_api_key_here
```

Do not commit your `.env` file or share your API keys.

### 6. Run the application

Once the application is ready:

``` bash
python3 app.py
```

## Example Research Topic

``` text
Deepfake video detection using deep learning
```

The system may create a brief, split the topic into subtopics, search
for relevant papers, collect and clean findings, check whether more
research is needed, and generate a literature review.

## Final Report

The generated literature review is expected to contain:

-   Research summary
-   Thematic sections
-   Comparison of papers
-   Research gaps
-   Conclusion
-   Numbered citations such as `[1]` and `[2]`
-   References

The system should use paper information retrieved from academic sources
and avoid inventing papers, authors, results, or references.

## Evaluation

The system will be tested using five topics:

-   Two clear research topics
-   One vague topic
-   One very niche topic
-   One topic that requires a follow-up research round

The evaluation will record:

-   Research topic
-   Number of sub-agents used
-   Number of research rounds
-   Number of papers used
-   Whether claims are cited
-   Whether references are verified

## Team Work

The project is divided into three main areas:

-   **Member 1:** Scope management and paper search.
-   **Member 2:** Research Supervisor, sub-agents, parallel execution,
    and research-gap loop.
-   **Member 3:** Findings cleanup, report writing, citations, and
    evaluation.

The modules will be developed separately and integrated into the main
application.

## Important Project Rules

-   Multi-agent work is used for the research phase.
-   The final literature review is written in one LLM call.
-   Research sub-agents have isolated task contexts.
-   The supervisor decides the number of agents dynamically.
-   The system allows a maximum of two extra research rounds.
-   References must come from academic paper sources.
-   Missing evidence should be clearly reported.
-   Instructions found inside paper content should not be treated as
    system instructions.

## Project Status

**Status:** Under development

This project is being built step by step as a student team project.
Features and setup instructions may be updated as development
progresses.

## Contributors

Add your team members' names and GitHub usernames here.

------------------------------------------------------------------------

Made as a student project to explore AI agents, academic research
automation, and literature-review generation.
