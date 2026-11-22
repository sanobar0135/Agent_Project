import React, { useEffect, useState } from "react";
import {
  Search,
  BookOpen,
  BrainCircuit,
  History,
  ExternalLink,
  Download,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  LoaderCircle,
  Layers3,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API = "http://127.0.0.1:8000/api";

export default function App() {
  const [topic, setTopic] = useState("");
  const [runId, setRunId] = useState("");
  const [run, setRun] = useState(null);
  const [history, setHistory] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  // Load research history
  const loadHistory = () => {
    fetch(API + "/history")
      .then((response) => response.json())
      .then(setHistory)
      .catch(() => {});
  };

  useEffect(() => {
    loadHistory();
  }, []);

  // Poll backend for research run updates
  useEffect(() => {
    if (!runId) return;

    let active = true;

    const tick = async () => {
      try {
        const response = await fetch(API + "/research/" + runId);
        const data = await response.json();

        if (active) {
          setRun(data);

          if (
            data.status === "completed" ||
            data.status === "failed"
          ) {
            setBusy(false);
            loadHistory();
          }
        }
      } catch (err) {
        if (active) {
          setError("Could not reach the backend. Is FastAPI running?");
        }
      }
    };

    tick();

    const timer = setInterval(tick, 2000);

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [runId]);

  // Start a new research run
  async function start() {
    setError("");
    setRun(null);

    if (topic.trim().length < 5) {
      setError("Please enter a research topic of at least 5 characters.");
      return;
    }

    setBusy(true);

    try {
      const response = await fetch(API + "/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) {
        throw new Error(
          (await response.text()) || "Request failed"
        );
      }

      const data = await response.json();
      setRunId(data.run_id);
    } catch (err) {
      setBusy(false);
      setError(err.message || "Unable to start research");
    }
  }

  // Open a previous research run
  function selectHistory(id) {
    setRunId(id);
    setBusy(true);
    setError("");
  }

  // Download the generated Markdown report
  function downloadReport() {
    if (!run?.report) return;

    const blob = new Blob([run.report], {
      type: "text/markdown",
    });

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");

    anchor.href = url;
    anchor.download = "literature_review.md";
    anchor.click();

    URL.revokeObjectURL(url);
  }

  const papers = run?.relevant_papers || [];

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brandicon">
            <BrainCircuit />
          </div>

          <div>
            <strong>Deep Research</strong>
            <small>Research agent workspace</small>
          </div>
        </div>

        <div className="navitem active">
          <Layers3 size={17} />
          Research workspace
        </div>

        <div className="navitem">
          <History size={17} />
          Research history
        </div>

        <div className="sidebottom">
          <div className="sidecard">
            <div className="dot"></div>
            <b>Local research engine</b>
            <small>FastAPI · arXiv · Groq</small>
          </div>
        </div>
      </aside>

      {/* Main workspace */}
      <main>
        {/* Header */}
        <header>
          <div>
            <h1>Research workspace</h1>
            <p>
              Explore academic literature with a multi-agent research workflow.
            </p>
          </div>

          <div className="live">
            <span />
            LOCAL WORKSPACE
          </div>
        </header>

        {/* Research input */}
        <section className="hero">
          <div className="heroicon">
            <BrainCircuit size={30} />
          </div>

          <h2>What would you like to research?</h2>

          <p>
            Enter a topic. Your supervisor will split it into research areas,
            search papers, evaluate coverage and synthesize a literature review.
          </p>

          <div className="inputbox">
            <textarea
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
              placeholder="e.g. Parameter-efficient fine-tuning methods for LLMs"
              rows="2"
              disabled={busy}
            />

            <button onClick={start} disabled={busy}>
              <Search size={17} />
              {busy ? "Researching…" : "Start research"}
            </button>
          </div>

          {error && (
            <div className="error">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <div className="chips">
            <span>Parallel agents</span>
            <span>Coverage evaluation</span>
            <span>arXiv papers</span>
            <span>Literature review</span>
          </div>
        </section>

        {/* Research results */}
        {run && (
          <section className="results">
            <div className="sectionhead">
              <div>
                <h2>Research run</h2>
                <small>{run.topic}</small>
              </div>

              <Status status={run.status} />
            </div>

            {/* Progress */}
            <div className="progress">
              <div
                className={`progressbar ${
                  run.status === "completed" ? "done" : ""
                }`}
              ></div>
            </div>

            <div className="stage">
              <LoaderCircle
                className={run.status === "running" ? "spin" : ""}
                size={17}
              />

              <span>{run.stage || run.status}</span>
            </div>

            {run.error && (
              <div className="error">
                <AlertCircle size={16} />
                {run.error}
              </div>
            )}

            {/* Supervisor plan */}
            {run.tasks?.length > 0 && (
              <>
                <h3>
                  Supervisor plan
                  <small>{run.tasks.length} subtopics</small>
                </h3>

                <div className="taskgrid">
                  {run.tasks.map((task, index) => (
                    <div className="task" key={index}>
                      <div className="tasknum">
                        {String(index + 1).padStart(2, "0")}
                      </div>

                      <b>{task.subtopic}</b>

                      <p>{task.objective}</p>
                    </div>
                  ))}
                </div>
              </>
            )}

            {/* Research statistics */}
            {run.papers && (
              <div className="stats">
                <Stat
                  label="Papers collected"
                  value={run.papers.length}
                />

                <Stat
                  label="Relevant papers"
                  value={papers.length}
                />

                <Stat
                  label="Research agents"
                  value={run.findings?.length || 0}
                />
              </div>
            )}

            {/* Relevant papers */}
            {papers.length > 0 && (
              <>
                <h3>
                  Relevant papers
                  <small>Selected by relevance filter</small>
                </h3>

                <div className="paperlist">
                  {papers.map((paper, index) => (
                    <div className="paper" key={index}>
                      <div>
                        <b>{paper.title}</b>

                        <small>
                          {(paper.authors || [])
                            .slice(0, 4)
                            .join(", ")}
                          {paper.authors?.length > 4
                            ? " et al."
                            : ""}
                          {" · "}
                          {paper.year || "Year n/a"}
                        </small>

                        <p>{paper.abstract}</p>
                      </div>

                      <a
                        href={paper.url}
                        target="_blank"
                        rel="noreferrer"
                        title="Open paper"
                      >
                        <ExternalLink size={17} />
                      </a>
                    </div>
                  ))}
                </div>
              </>
            )}

            {/* Literature review */}
            {run.report && (
              <>
                <div className="reporthead">
                  <h3>Literature review</h3>

                  <button
                    className="secondary"
                    onClick={downloadReport}
                  >
                    <Download size={16} />
                    Download Markdown
                  </button>
                </div>

                <div className="report markdown-report">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {run.report}
                  </ReactMarkdown>
                </div>
              </>
            )}
          </section>
        )}

        {/* Research history */}
        <section className="history">
          <div className="sectionhead">
            <div>
              <h2>
                <History size={19} />
                Research history
              </h2>

              <small>Saved local runs</small>
            </div>

            <button
              className="secondary"
              onClick={loadHistory}
            >
              <RefreshCw size={15} />
              Refresh
            </button>
          </div>

          {history.length === 0 ? (
            <div className="empty">
              Your completed and recent research runs will appear here.
            </div>
          ) : (
            history.map((item) => (
              <button
                className="historyrow"
                key={item.id}
                onClick={() => selectHistory(item.id)}
              >
                <div>
                  <b>{item.topic}</b>
                  <small>{item.created_at}</small>
                </div>

                <Status status={item.status} />
              </button>
            ))
          )}
        </section>

        {/* Footer */}
        <footer>
          <BookOpen size={15} />
          Evidence-based research assistance · Validate findings and references
          before use.
        </footer>
      </main>
    </div>
  );
}

// Status component
function Status({ status }) {
  let cls =
    status === "completed"
      ? "good"
      : status === "failed"
      ? "bad"
      : "pending";

  return (
    <span className={`status ${cls}`}>
      {status === "completed" ? (
        <>
          <CheckCircle2 size={14} />
          completed
        </>
      ) : status === "failed" ? (
        <>
          <AlertCircle size={14} />
          failed
        </>
      ) : (
        <>
          <LoaderCircle size={14} />
          {status}
        </>
      )}
    </span>
  );
}

// Statistics component
function Stat({ label, value }) {
  return (
    <div className="stat">
      <strong>{value}</strong>
      <small>{label}</small>
    </div>
  );
}