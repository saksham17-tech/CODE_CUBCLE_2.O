# DataForge AI — Hackathon MVP

**The Autonomous AI Data Intelligence & Automation Platform**

National Level Hackathon — Corporate Digital Intelligence & Automation Track

## Quick Start

```bash
cd dataforge-backend
pip install -r requirements.txt
# (or: pip install fastapi uvicorn sqlalchemy aiosqlite greenlet pydantic httpx beautifulsoup4)
PYTHONPATH=. python3 run_demo.py
```

Open **http://127.0.0.1:8765** in your browser.

API docs: **http://127.0.0.1:8765/docs**

## What this MVP demonstrates

| PRD Feature | Status |
|-------------|--------|
| Natural-language prompt → structured intent | ✅ |
| Editable visual DAG workflow plan | ✅ |
| Compliance checks (allowlist + robots.txt note) | ✅ |
| Source connectors (simulated realistic data) | ✅ |
| Validation + confidence scoring | ✅ |
| Deduplication | ✅ |
| Full provenance / lineage per field | ✅ |
| Task manager with live logs & progress | ✅ |
| Results explorer (filterable table) | ✅ |
| Export CSV / JSON | ✅ |
| Workflow history | ✅ |
| Cost/time estimator + sandbox dry-run | ✅ |

## Example prompts

- `Collect all Senior Data Engineer openings in Bengaluru posted this week across permitted job boards.`
- `Find 15 mid-size SaaS companies in India that raised funding in the last 6 months, with founder LinkedIn and company email.`
- `Find companies that sponsored fintech conferences in the last year, with contact details.`

## Architecture (matches PRD §7)

```
Experience Layer (static HTML + Tailwind) 
    ↓
Intelligence Layer (intent parser + DAG planner)
    ↓
Orchestration Layer (workflow runner)
    ↓
Collection Layer (permitted sources → realistic demo datasets)
    ↓
Trust & Data Layer (SQLite + provenance + confidence)
```

## Project layout

```
dataforge-backend/
├── app/
│   ├── main.py              # FastAPI app + static UI
│   ├── db/database.py
│   ├── models/models.py     # User, Workflow, TaskRun, Record, FieldProvenance...
│   ├── routers/workflows.py # Full API surface
│   └── services/
│       ├── intent_parser.py # NL → structured intent + DAG
│       ├── collector.py     # Source connectors + demo data
│       └── orchestrator.py  # DAG execution + lineage
├── static/index.html        # Command-center dark UI
├── run_demo.py
└── requirements.txt
```

## Notes for judges / further build

- LLM is currently a high-quality rule + template system that mirrors Claude-style structured output (swap in Claude API in `intent_parser.py` for production).
- Scraping uses realistic synthetic data for demo reliability; Playwright connectors can be plugged into the same interface.
- Frontend also exists as a Next.js app under `../dataforge-frontend` (dark theme matching PRD §10).

Built for the 36-hour hackathon build plan (PRD §16).
