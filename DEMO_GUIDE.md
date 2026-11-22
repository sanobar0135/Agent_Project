# Monday demo (3–5 minutes)
1. Start FastAPI and Vite in separate terminals.
2. Enter `Parameter-efficient fine-tuning methods for LLMs`.
3. Launch research and show the supervisor plan.
4. Show progress stage, paper records and relevant-paper list.
5. Explain coverage feedback and bounded additional research.
6. Show the synthesis and download the Markdown report.
7. Show history and reload the saved run.

## Architecture
React UI → FastAPI → existing Python research modules → Groq planning/evaluation/synthesis + arXiv retrieval → SQLite history → UI.

## Limitations
- arXiv is the retrieval source in this version.
- The LLM analysis is based on paper metadata/abstracts and should be verified.
- Progress updates are stage-based, not token-level.
- No authentication; this is a local demo application.
- API availability and latency depend on network and provider services.
