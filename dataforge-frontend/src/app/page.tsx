"use client";

import { useState, useEffect, useCallback } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type View = "home" | "planner" | "task" | "results" | "history";

interface WorkflowPlan {
  workflow_id: number;
  structured_intent: any;
  dag: any;
  estimate: any;
}

interface TaskStatus {
  id: number;
  status: string;
  progress: number;
  records_collected: number;
  logs: { ts: string; msg: string }[];
  error_log?: string;
}

export default function DataForgeApp() {
  const [view, setView] = useState<View>("home");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<WorkflowPlan | null>(null);
  const [task, setTask] = useState<TaskStatus | null>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const examplePrompts = [
    "Collect all Senior Data Engineer openings in Bengaluru posted this week across permitted job boards.",
    "Find 15 mid-size SaaS companies in India that raised funding in the last 6 months, with founder LinkedIn and company email.",
    "Find companies that sponsored fintech conferences in the last year, with contact details.",
  ];

  const submitPrompt = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/workflows`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setPlan(data);
      setView("planner");
    } catch (e: any) {
      setError(e.message || "Failed to parse intent");
    } finally {
      setLoading(false);
    }
  };

  const runWorkflow = async (dry = false) => {
    if (!plan) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/workflows/${plan.workflow_id}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dry_run: dry }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (dry) {
        alert(data.message);
        setLoading(false);
        return;
      }
      setTask({ id: data.task_run_id, status: "queued", progress: 0, records_collected: 0, logs: [] });
      setView("task");
      pollTask(data.task_run_id);
    } catch (e: any) {
      setError(e.message);
      setLoading(false);
    }
  };

  const pollTask = useCallback(async (runId: number) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API}/api/tasks/${runId}`);
        const data = await res.json();
        setTask(data);
        if (data.status === "completed" || data.status === "failed") {
          clearInterval(interval);
          setLoading(false);
          if (data.status === "completed" && plan) {
            loadRecords(plan.workflow_id);
          }
        }
      } catch {
        /* ignore transient */
      }
    }, 800);
    // safety clear
    setTimeout(() => clearInterval(interval), 60000);
  }, [plan]);

  const loadRecords = async (wfId: number) => {
    const res = await fetch(`${API}/api/datasets/${wfId}/records?limit=100`);
    const data = await res.json();
    setRecords(data.records || []);
    setView("results");
  };

  const loadHistory = async () => {
    const res = await fetch(`${API}/api/workflows`);
    const data = await res.json();
    setHistory(data || []);
    setView("history");
  };

  const exportData = async (format = "json") => {
    if (!plan) return;
    const res = await fetch(`${API}/api/datasets/${plan.workflow_id}/export?format=${format}`, {
      method: "POST",
    });
    const data = await res.json();
    if (format === "csv" && data.content) {
      const blob = new Blob([data.content], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = data.filename || "dataforge_export.csv";
      a.click();
    } else {
      const blob = new Blob([JSON.stringify(data.content, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `dataforge_${plan.workflow_id}.json`;
      a.click();
    }
  };

  // ---- UI pieces ----
  const Header = () => (
    <header className="border-b border-zinc-800 bg-[#0a0a0b]/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setView("home")}>
          <div className="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center font-bold text-black text-sm">
            DF
          </div>
          <span className="font-semibold tracking-tight">
            DataForge <span className="text-orange-500">AI</span>
          </span>
        </div>
        <nav className="flex items-center gap-1 text-sm">
          {[
            { id: "home", label: "Prompt" },
            { id: "history", label: "History" },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => (item.id === "history" ? loadHistory() : setView(item.id as View))}
              className={`px-3 py-1.5 rounded-md transition ${
                view === item.id ? "bg-zinc-800 text-orange-400" : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-950/50 border border-red-800 text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* ===== HOME / PROMPT CONSOLE ===== */}
        {view === "home" && (
          <div className="max-w-3xl mx-auto space-y-8">
            <div className="text-center space-y-3">
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">
                Describe what data you need
              </h1>
              <p className="text-zinc-400 text-lg">
                DataForge turns a plain-English request into a source-backed, validated dataset —
                zero custom scrapers required.
              </p>
            </div>

            <div className="bg-[#141416] border border-zinc-800 rounded-2xl p-1 shadow-2xl shadow-orange-500/5">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g. Find 100 mid-size SaaS companies in India that raised funding in the last 6 months..."
                rows={4}
                className="w-full bg-transparent px-4 py-3 text-base resize-none focus:outline-none placeholder:text-zinc-600"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submitPrompt();
                }}
              />
              <div className="flex items-center justify-between px-3 pb-2">
                <span className="text-xs text-zinc-600">⌘ + Enter to submit</span>
                <button
                  onClick={submitPrompt}
                  disabled={loading || !prompt.trim()}
                  className="px-5 py-2 rounded-lg bg-orange-500 hover:bg-orange-400 disabled:opacity-40 text-black font-semibold text-sm transition"
                >
                  {loading ? "Planning…" : "Generate Plan"}
                </button>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-xs text-zinc-500 uppercase tracking-wider">Try an example</p>
              <div className="flex flex-wrap gap-2">
                {examplePrompts.map((ex, i) => (
                  <button
                    key={i}
                    onClick={() => setPrompt(ex)}
                    className="text-left text-sm px-3 py-2 rounded-lg bg-zinc-900 border border-zinc-800 hover:border-orange-500/50 text-zinc-300 transition max-w-full"
                  >
                    {ex.length > 80 ? ex.slice(0, 80) + "…" : ex}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-6 border-t border-zinc-900">
              {[
                { label: "< 2 min", desc: "Prompt → first dataset" },
                { label: "100%", desc: "Records with source + confidence" },
                { label: "0 lines", desc: "Custom scraper code needed" },
              ].map((s) => (
                <div key={s.label} className="text-center">
                  <div className="text-2xl font-bold text-orange-500">{s.label}</div>
                  <div className="text-xs text-zinc-500 mt-1">{s.desc}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ===== WORKFLOW PLANNER ===== */}
        {view === "planner" && plan && (
          <div className="space-y-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold">Workflow Plan</h2>
                <p className="text-zinc-400 text-sm mt-1">Review & edit before execution · Transparent AI planning</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => runWorkflow(true)}
                  className="px-4 py-2 rounded-lg border border-zinc-700 text-sm hover:bg-zinc-900"
                >
                  Sandbox Dry-Run
                </button>
                <button
                  onClick={() => runWorkflow(false)}
                  disabled={loading}
                  className="px-5 py-2 rounded-lg bg-orange-500 hover:bg-orange-400 text-black font-semibold text-sm disabled:opacity-50"
                >
                  {loading ? "Starting…" : "Approve & Run"}
                </button>
              </div>
            </div>

            {/* Intent card */}
            <div className="bg-[#141416] border border-zinc-800 rounded-xl p-5">
              <h3 className="text-sm font-medium text-zinc-400 mb-3">Structured Intent</h3>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-zinc-500">Entity</span>
                  <p className="font-mono text-orange-400">{plan.structured_intent.entity_type}</p>
                </div>
                <div>
                  <span className="text-zinc-500">Limit</span>
                  <p className="font-mono">{plan.structured_intent.limit}</p>
                </div>
                <div>
                  <span className="text-zinc-500">Sources</span>
                  <p className="font-mono text-xs">{plan.structured_intent.preferred_sources?.join(", ")}</p>
                </div>
                <div>
                  <span className="text-zinc-500">Est. time / cost</span>
                  <p className="font-mono">
                    ~{plan.estimate?.estimated_seconds}s · ${plan.estimate?.estimated_cost_usd}
                  </p>
                </div>
              </div>
              <div className="mt-3 pt-3 border-t border-zinc-800">
                <span className="text-zinc-500 text-sm">Fields: </span>
                <span className="text-sm font-mono">
                  {plan.structured_intent.required_fields?.join(" · ")}
                </span>
              </div>
            </div>

            {/* DAG visual */}
            <div className="bg-[#141416] border border-zinc-800 rounded-xl p-5">
              <h3 className="text-sm font-medium text-zinc-400 mb-4">Execution DAG</h3>
              <div className="flex flex-wrap items-center gap-2">
                {plan.dag?.nodes?.map((node: any, idx: number) => (
                  <div key={node.id} className="flex items-center gap-2">
                    <div className="px-4 py-3 rounded-lg bg-zinc-900 border border-zinc-700 min-w-[140px]">
                      <div className="text-xs text-orange-400 font-medium uppercase">{node.type}</div>
                      <div className="text-sm font-medium mt-0.5">{node.label}</div>
                      <div className="text-xs text-zinc-500 mt-1">{node.estimated_time_sec}s</div>
                    </div>
                    {idx < plan.dag.nodes.length - 1 && (
                      <span className="text-zinc-600 text-lg">→</span>
                    )}
                  </div>
                ))}
              </div>
              <p className="text-xs text-zinc-500 mt-4 flex items-center gap-1">
                <span className="inline-block w-2 h-2 rounded-full bg-green-500" />
                Compliance: all sources checked against allowlist + robots.txt
              </p>
            </div>

            <button onClick={() => setView("home")} className="text-sm text-zinc-500 hover:text-zinc-300">
              ← Back to prompt
            </button>
          </div>
        )}

        {/* ===== TASK MANAGER ===== */}
        {view === "task" && task && (
          <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">Task Running</h2>
            <div className="bg-[#141416] border border-zinc-800 rounded-xl p-6 space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-zinc-400">Status</span>
                <span
                  className={`font-mono capitalize ${
                    task.status === "completed"
                      ? "text-green-400"
                      : task.status === "failed"
                      ? "text-red-400"
                      : "text-orange-400"
                  }`}
                >
                  {task.status}
                </span>
              </div>
              <div>
                <div className="flex justify-between text-xs text-zinc-500 mb-1">
                  <span>Progress</span>
                  <span>{Math.round(task.progress || 0)}%</span>
                </div>
                <div className="h-2 bg-zinc-900 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-orange-500 transition-all duration-500"
                    style={{ width: `${task.progress || 0}%` }}
                  />
                </div>
              </div>
              {task.records_collected > 0 && (
                <p className="text-sm text-zinc-300">
                  Collected <strong className="text-orange-400">{task.records_collected}</strong> records
                </p>
              )}
              <div className="bg-black/40 rounded-lg p-3 max-h-48 overflow-y-auto font-mono text-xs space-y-1">
                {(task.logs || []).map((l, i) => (
                  <div key={i} className="text-zinc-400">
                    <span className="text-zinc-600">{l.ts?.slice(11, 19)}</span> {l.msg}
                  </div>
                ))}
              </div>
              {task.status === "completed" && (
                <button
                  onClick={() => plan && loadRecords(plan.workflow_id)}
                  className="w-full py-2.5 rounded-lg bg-orange-500 text-black font-semibold text-sm"
                >
                  Explore Results →
                </button>
              )}
            </div>
          </div>
        )}

        {/* ===== RESULTS EXPLORER ===== */}
        {view === "results" && (
          <div className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-2xl font-bold">Results Explorer</h2>
                <p className="text-zinc-400 text-sm">
                  {records.length} source-backed records · every field traceable
                </p>
              </div>
              <div className="flex gap-2">
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Filter…"
                  className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-700 text-sm w-40 focus:outline-none focus:border-orange-500"
                />
                <button
                  onClick={() => exportData("csv")}
                  className="px-3 py-1.5 rounded-lg border border-zinc-700 text-sm hover:bg-zinc-900"
                >
                  Export CSV
                </button>
                <button
                  onClick={() => exportData("json")}
                  className="px-3 py-1.5 rounded-lg border border-zinc-700 text-sm hover:bg-zinc-900"
                >
                  Export JSON
                </button>
              </div>
            </div>

            <div className="overflow-x-auto rounded-xl border border-zinc-800">
              <table className="w-full text-sm">
                <thead className="bg-zinc-900 text-zinc-400 text-left">
                  <tr>
                    <th className="px-4 py-3 font-medium">#</th>
                    {records[0] &&
                      Object.keys(records[0])
                        .filter((k) => !["id", "entity_type", "confidence_score", "dedup_cluster_id", "created_at"].includes(k))
                        .slice(0, 6)
                        .map((k) => (
                          <th key={k} className="px-4 py-3 font-medium capitalize">
                            {k.replace(/_/g, " ")}
                          </th>
                        ))}
                    <th className="px-4 py-3 font-medium">Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {records
                    .filter((r) => {
                      if (!search) return true;
                      return JSON.stringify(r).toLowerCase().includes(search.toLowerCase());
                    })
                    .map((r, i) => (
                      <tr key={r.id || i} className="border-t border-zinc-800/80 hover:bg-zinc-900/50">
                        <td className="px-4 py-2.5 text-zinc-500 font-mono text-xs">{r.id}</td>
                        {Object.keys(r)
                          .filter((k) => !["id", "entity_type", "confidence_score", "dedup_cluster_id", "created_at"].includes(k))
                          .slice(0, 6)
                          .map((k) => (
                            <td key={k} className="px-4 py-2.5 max-w-[180px] truncate">
                              {typeof r[k] === "string" && r[k].startsWith("http") ? (
                                <a href={r[k]} target="_blank" rel="noreferrer" className="text-orange-400 hover:underline">
                                  link
                                </a>
                              ) : (
                                String(r[k] ?? "")
                              )}
                            </td>
                          ))}
                        <td className="px-4 py-2.5">
                          <span
                            className={`inline-block px-2 py-0.5 rounded text-xs font-mono ${
                              (r.confidence_score || 0) >= 0.9
                                ? "bg-green-950 text-green-400"
                                : "bg-yellow-950 text-yellow-400"
                            }`}
                          >
                            {((r.confidence_score || 0) * 100).toFixed(0)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
            <button onClick={() => setView("home")} className="text-sm text-zinc-500 hover:text-zinc-300">
              ← New prompt
            </button>
          </div>
        )}

        {/* ===== HISTORY ===== */}
        {view === "history" && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Workflow History</h2>
            <div className="space-y-2">
              {history.length === 0 && <p className="text-zinc-500">No workflows yet.</p>}
              {history.map((w) => (
                <div
                  key={w.id}
                  className="flex items-center justify-between p-4 rounded-xl bg-[#141416] border border-zinc-800 hover:border-zinc-700 cursor-pointer"
                  onClick={() => {
                    if (w.status === "completed") {
                      setPlan({ workflow_id: w.id } as any);
                      loadRecords(w.id);
                    }
                  }}
                >
                  <div>
                    <p className="text-sm font-medium">{w.prompt_text}</p>
                    <p className="text-xs text-zinc-500 mt-1">
                      {w.entity_type} · {w.created_at?.slice(0, 19)}
                    </p>
                  </div>
                  <span
                    className={`text-xs px-2 py-1 rounded font-mono ${
                      w.status === "completed"
                        ? "bg-green-950 text-green-400"
                        : w.status === "running"
                        ? "bg-orange-950 text-orange-400"
                        : "bg-zinc-800 text-zinc-400"
                    }`}
                  >
                    {w.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-zinc-900 py-4 text-center text-xs text-zinc-600">
        DataForge AI · National Level Hackathon MVP · Source-backed · Compliance by design
      </footer>
    </div>
  );
}
