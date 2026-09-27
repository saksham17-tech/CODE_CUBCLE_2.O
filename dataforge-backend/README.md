# DataForge AI

**The Autonomous AI Data Intelligence & Automation Platform**

> Prompt-driven · Source-backed · Compliance by design

National Level Hackathon — Corporate Digital Intelligence & Automation Track  
**Version:** 1.0 — Hackathon Submission Build

---

## Overview

DataForge AI turns a single plain-English request into a fully autonomous, source-backed data collection pipeline.

Instead of engineers hand-building a new scraper for every business need (job openings today, sponsor leads tomorrow, competitor pricing next week), a user simply describes what they need. DataForge:

1. Interprets the request  
2. Designs an editable execution plan (DAG)  
3. Collects data only from permitted & compliant sources  
4. Cleans, validates, and deduplicates  
5. Surfaces results in a live dashboard with full provenance  

**Key numbers (from PRD):**

| Metric | Target |
|--------|--------|
| Time to first structured dataset | < 2 minutes |
| Records with source URL + confidence | 100% |
| Custom scraper code required from user | 0 lines |

---

## Features (MVP)

### Core
- **Natural-language intent capture** — describe data needs in plain English  
- **Intent parser** — converts prompt → structured spec (entities, fields, filters, sources)  
- **Dynamic workflow generator** — builds an editable DAG (search → extract → validate → dedup → store)  
- **Workflow orchestrator** — executes nodes, tracks progress, logs every step  
- **Source connectors** — web search, permitted-site scraping, public APIs, RSS (pluggable)  
- **Data processing** — cleaning, normalization, schema mapping, confidence scoring  
- **Deduplication** — near-duplicate merge across sources  
- **Task manager** — live progress, logs, status (queued / running / completed / failed)  
- **Results explorer** — searchable, filterable table with confidence scores  
- **Source inspector & lineage** — every field traceable to URL + timestamp  
- **Export center** — one-click CSV / JSON  
- **Workflow history** — save, re-run, and revisit past pipelines  

### Differentiator highlights (shown in UI)
- Transparent, editable AI plan before execution  
- Trust & compliance layer (allowlist + robots.txt note)  
- Cost / time estimator + sandbox dry-run  
- Full field-level provenance  

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML + Tailwind CSS (dark command-center theme) |
| Backend | FastAPI (Python) |
| Database | SQLite (in-memory with StaticPool for demo) |
| Orchestration | Async workflow runner |
| Data | BeautifulSoup-ready connectors + realistic demo datasets |

Optional Next.js frontend also included under `dataforge-frontend/`.

---

## Quick Start

### 1. Prerequisites
- Python **3.8 – 3.12** (3.11+ recommended)
- `pip`

### 2. Install

```bash
cd dataforge-backend
python -m pip install -r requirements.txt
```

### 3. Run

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
python run_demo.py
```

**macOS / Linux:**
```bash
PYTHONPATH=. python run_demo.py
# or
PYTHONPATH=. python3 run_demo.py
```

### 4. Open the app
- **UI:**      http://127.0.0.1:8765  
- **API docs:** http://127.0.0.1:8765/docs  
- **Health:**   http://127.0.0.1:8765/health  

---

## Example Prompts

Try these in the Prompt Console:

```
Collect all Senior Data Engineer openings in Bengaluru posted this week across permitted job boards.
```

```
Find 15 mid-size SaaS companies in India that raised funding in the last 6 months, with founder LinkedIn and company email.
```

```
Find companies that sponsored fintech conferences in the last year, with contact details.
```

**Flow:**  
Prompt → AI generates plan (intent + DAG) → Review / Sandbox dry-run → **Approve & Run** → Live progress → Results explorer → Export CSV/JSON

---

## Project Structure

```
dataforge-backend/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run_demo.py               # Start server (port 8765)
├── app/
│   ├── main.py               # FastAPI app + static UI mount
│   ├── db/
│   │   └── database.py       # Async SQLAlchemy + SQLite
│   ├── models/
│   │   └── models.py         # User, Workflow, TaskRun, Record, Provenance...
│   ├── routers/
│   │   └── workflows.py      # Full REST API surface
│   └── services/
│       ├── intent_parser.py  # NL → structured intent + DAG planner
│       ├── collector.py      # Source connectors + demo data
│       └── orchestrator.py   # DAG execution, validation, lineage
└── static/
    └── index.html            # Full interactive dashboard UI
```

---

## API Surface (selected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/workflows` | Submit NL prompt → structured intent + DAG plan |
| `POST` | `/api/workflows/{id}/run` | Approve plan and execute (or dry-run) |
| `GET`  | `/api/workflows/{id}` | Fetch workflow definition & status |
| `GET`  | `/api/workflows` | List recent workflows |
| `GET`  | `/api/tasks/{run_id}` | Live progress, logs, status |
| `GET`  | `/api/datasets/{id}/records` | Query collected records |
| `GET`  | `/api/datasets/{id}/lineage` | Provenance graph |
| `POST` | `/api/datasets/{id}/export` | Export CSV or JSON |
| `GET`  | `/api/sources/allowlist` | Permitted sources |

Interactive docs available at `/docs` (Swagger UI).

---

## End-to-End Lifecycle (matches PRD)

1. **Prompt submission** — user types requirement  
2. **Intent parsing** — entities, fields, filters, preferred sources  
3. **Workflow planning** — editable DAG generated  
4. **Review & approval** — user can dry-run or approve  
5. **Compliance check** — allowlist / robots.txt  
6. **Execution** — connectors fetch from permitted sources  
7. **Processing & validation** — schema + confidence scores  
8. **Deduplication** — near-duplicate merge  
9. **Storage & lineage** — every field keeps source URL + timestamp  
10. **Explore / Export** — results table, CSV/JSON download  

---

## Notes for Judges & Further Development

- **LLM layer:** Currently a high-quality rule + template engine that produces realistic structured intents and DAGs. Swap in Claude / OpenAI in `intent_parser.py` for production-grade NL understanding.  
- **Collection layer:** Uses realistic synthetic datasets for reliable demos. The connector interface is ready for Playwright, real public APIs, and RSS.  
- **Compliance:** Allowlist-first design; every collection path is designed to respect robots.txt and rate limits.  
- **Frontend:** Primary demo UI is the dark “command-center” static app. A Next.js scaffold (`dataforge-frontend/`) is included for teams that want a React SPA.  
- **Database:** In-memory SQLite with `StaticPool` for zero-setup demo. Switch `DATABASE_URL` in `app/db/database.py` to a file or PostgreSQL for persistence.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `sqlalchemy==2.1.1` install fails | Use the provided `requirements.txt` (pins `<2.1.0`). Needs Python ≥ 3.8. |
| `ModuleNotFoundError: No module named 'app'` | Set `PYTHONPATH=.` (or `$env:PYTHONPATH="."` on Windows) before running. |
| Port 8765 already in use | Edit port in `run_demo.py` or kill the existing process. |
| Blank page / API errors | Confirm server is running and open http://127.0.0.1:8765 (not localhost if IPv6 issues). |

---

## License & Attribution

Built for the **National Level Hackathon — Corporate Digital Intelligence & Automation Track**.

Product concept and requirements derived from the official DataForge AI PRD (v1.0).

---

**DataForge AI** — Make organizational data-gathering as simple as asking a question.
