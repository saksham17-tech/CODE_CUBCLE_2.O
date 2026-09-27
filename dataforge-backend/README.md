# DataForge AI

**The Autonomous AI Data Intelligence & Automation Platform**

> Prompt-driven · Source-backed · Compliance by design · Accurate filters

National Level Hackathon — Corporate Digital Intelligence & Automation Track  
**Version:** 1.2 — Expanded domains + Watchtower + Chat + Insights

---

## Problem statement (what we solve)

Businesses need web data (jobs, leads, sponsors, market intel, articles) but building a new scraper per requirement does not scale.

**DataForge AI** lets users describe needs in plain English. The system:

1. Parses intent (entity, filters, sources, limit)  
2. Builds an editable execution DAG  
3. Collects only from permitted sources  
4. Validates, scores confidence, deduplicates  
5. Stores full lineage and exposes explore / chat / export / monitor  

**Expected outcome:** natural-language requirement → clean, structured, source-backed dataset with a managed workflow.

---

## Supported data domains (diversified)

| Domain | Example prompt | Key filters |
|--------|----------------|-------------|
| **Jobs** | `Data Science jobs in Noida` | title, location, seniority, industry, posted_within |
| **Company leads** | `10 SaaS companies in India that raised funding` | industry, location, size, funding window |
| **Sponsors / events** | `Companies that sponsored fintech conferences` | industry, location |
| **Articles / news** | `20 most viral articles for JEE` | topic, sort=viral/recent |
| **Products** | `Top AI tools on Product Hunt` | category |
| **GitHub repos** | `Open source ML repositories` | topic |
| **Pricing** | `Compare Notion Figma Slack pricing` | — |

**Locations understood:** Bengaluru, Mumbai, Delhi/NCR, Hyderabad, Chennai, Pune, Noida, Gurgaon, Kolkata, Remote, India, and more.

**Job titles understood:** Data Scientist, Data Analyst, Data Engineer, Backend/Frontend/Full Stack, ML/AI Engineer, DevOps, SRE, PM, QA, Android/iOS, and more.

**Article topics:** JEE, NEET, AI, Fintech, Startups, Technology, Education, …

---

## Feature set

### Core (problem brief)
- [x] Natural-language intent capture  
- [x] Dynamic workflow DAG (search → extract → validate → dedup → store)  
- [x] Permitted-source collection + compliance note  
- [x] Clean / structure / validate / confidence scores  
- [x] Deduplication  
- [x] Task progress + logs  
- [x] Results explorer  
- [x] Source-backed URLs (real career pages + job-board searches)  
- [x] Workflow history  
- [x] Search / filter / export CSV & JSON  

### Differentiator features
- [x] **Transparent plan review** before run + sandbox dry-run  
- [x] **Cost / time estimator**  
- [x] **Field-level lineage** API  
- [x] **Watchtower monitors** — promote any workflow to recurring schedule  
- [x] **Chat-with-your-data** — ask counts, companies, locations, roles  
- [x] **Auto insights** — breakdowns by location, company, title, topic  
- [x] **Strict filter accuracy** — title + city must match the prompt  

---

## Quick start

```bash
cd dataforge-backend
python -m pip install -r requirements.txt
```

**Windows PowerShell**
```powershell
$env:PYTHONPATH = "."
python run_demo.py
```

**macOS / Linux**
```bash
PYTHONPATH=. python3 run_demo.py
```

- UI: http://127.0.0.1:8765  
- API docs: http://127.0.0.1:8765/docs  

Requires **Python 3.8–3.12**.

---

## Example prompts (accuracy-focused)

```
Find all job openings for Data Science role in Noida region
```
→ Only **Data Scientist** titles, only **Noida** companies.

```
Collect Senior Backend Engineer jobs in Mumbai posted this week
```
→ Senior Backend Engineer + Mumbai only.

```
Find me 20 most viral articles for JEE
```
→ 20 JEE education articles sorted by engagement (views).

```
Find 10 mid-size SaaS companies in India that raised funding
```
→ SaaS leads with funding stage + websites.

```
Top AI tools and products on Product Hunt
```
→ Product directory with upvotes + pricing model.

```
Popular open source GitHub repositories for machine learning
```
→ Real GitHub project links with stars + language.

---

## API surface

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/workflows` | Prompt → intent + DAG |
| POST | `/api/workflows/{id}/run` | Execute or dry-run |
| GET | `/api/workflows` | History |
| GET | `/api/tasks/{id}` | Progress + logs |
| GET | `/api/datasets/{id}/records` | Records (+ `?search=`) |
| GET | `/api/datasets/{id}/lineage` | Provenance graph |
| GET | `/api/datasets/{id}/insights` | Auto stats |
| POST | `/api/datasets/{id}/chat` | NL Q&A over dataset |
| POST | `/api/datasets/{id}/export` | CSV / JSON |
| POST | `/api/monitors` | Create Watchtower monitor |
| GET | `/api/monitors` | List monitors |
| GET | `/api/sources/allowlist` | Permitted sources |

---

## Project structure

```
dataforge-backend/
├── README.md
├── requirements.txt
├── run_demo.py
├── app/
│   ├── main.py
│   ├── db/database.py
│   ├── models/models.py
│   ├── routers/workflows.py
│   └── services/
│       ├── intent_parser.py   # NL → structured intent + DAG
│       ├── collector.py       # Domain datasets + filter enforcement
│       └── orchestrator.py    # Execute pipeline + lineage
└── static/index.html          # Dark command-center UI
```

---

## Accuracy principles

1. **Parse first** — location, title, topic, limit, seniority extracted before any data is generated.  
2. **Filter hard** — collector only emits rows that match location + title/topic/industry.  
3. **Real links** — job board *search* URLs and real company career pages (no fake job IDs).  
4. **No silent generic dump** — unclassified prompts get Google search links, not random junk rows labeled as jobs.  
5. **Confidence scores** on every record; lineage retained per field.

---

## Tech stack

FastAPI · SQLAlchemy (async SQLite) · Tailwind UI · rule-based intent planner (swap-in LLM ready)

---

## Changelog

### v1.2
- Diversified domains: articles, products, GitHub, pricing  
- Strict Data Science / Noida (and general title+city) accuracy  
- Viral article ranking by engagement  
- Watchtower monitors, Chat-with-data, Auto insights  
- Expanded Indian company + city coverage  
- Real working source URLs  

### v1.1
- Location & title filter fixes, faster runs, README  

### v1.0
- Initial hackathon MVP  

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Wrong roles/cities | Restart from **this** zip; run a **new** prompt (old history is stale). |
| `sqlalchemy 2.1` install error | Use provided requirements (`sqlalchemy>=2.0,<2.1`). |
| `No module named app` | Set `PYTHONPATH=.` |
| Port in use | Change port in `run_demo.py` or stop the other process. |

---

**DataForge AI** — organizational data-gathering as simple as asking a question, with filters you can trust.
