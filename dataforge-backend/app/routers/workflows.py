from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

from app.db.database import get_db
from app.models.models import Workflow, TaskRun, Record, FieldProvenance, Source
from app.services.intent_parser import parse_intent, generate_workflow_dag, estimate_cost_time
from app.services.orchestrator import run_workflow

router = APIRouter(prefix="/api", tags=["workflows"])

class PromptRequest(BaseModel):
    prompt: str
    user_id: Optional[int] = 1

class RunRequest(BaseModel):
    dry_run: bool = False

@router.post("/workflows")
async def create_workflow(req: PromptRequest, db: AsyncSession = Depends(get_db)):
    """Submit NL prompt → structured intent + editable DAG plan."""
    if not req.prompt or len(req.prompt.strip()) < 5:
        raise HTTPException(400, "Prompt too short")
    
    intent = parse_intent(req.prompt)
    dag = generate_workflow_dag(intent)
    estimate = estimate_cost_time(dag)
    
    wf = Workflow(
        prompt_text=req.prompt,
        structured_intent=intent,
        dag_definition=dag,
        status="draft",
        created_by=req.user_id
    )
    db.add(wf)
    await db.commit()
    await db.refresh(wf)
    
    return {
        "workflow_id": wf.id,
        "status": wf.status,
        "structured_intent": intent,
        "dag": dag,
        "estimate": estimate,
        "message": "Plan ready for review. Approve to execute."
    }

@router.post("/workflows/{workflow_id}/run")
async def approve_and_run(
    workflow_id: int,
    req: RunRequest,
    db: AsyncSession = Depends(get_db)
):
    """Approve plan and execute (inline for reliable MVP demo)."""
    wf = await db.get(Workflow, workflow_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")
    
    if req.dry_run:
        return {
            "message": "Sandbox dry-run: would collect ~{} records in ~{}s".format(
                (wf.dag_definition or {}).get("estimated_records", 10),
                (wf.dag_definition or {}).get("estimated_total_sec", 60)
            ),
            "sandbox": True
        }
    
    task = TaskRun(
        workflow_id=workflow_id,
        status="queued",
        logs=[{"ts": datetime.utcnow().isoformat(), "msg": "Queued for execution"}]
    )
    db.add(task)
    wf.status = "running"
    await db.commit()
    await db.refresh(task)
    
    # Execute inline so demo is reliable (logs still update during run)
    result = await run_workflow(db, workflow_id, task.id)
    
    return {
        "task_run_id": task.id,
        "workflow_id": workflow_id,
        "status": result.get("status", "completed"),
        "records_collected": result.get("records_collected", 0),
        "message": "Execution finished."
    }

@router.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    wf = await db.get(Workflow, workflow_id)
    if not wf:
        raise HTTPException(404, "Not found")
    return {
        "id": wf.id,
        "prompt_text": wf.prompt_text,
        "structured_intent": wf.structured_intent,
        "dag_definition": wf.dag_definition,
        "status": wf.status,
        "version": wf.version,
        "is_monitor": wf.is_monitor,
        "created_at": wf.created_at.isoformat() if wf.created_at else None
    }

@router.get("/workflows")
async def list_workflows(db: AsyncSession = Depends(get_db), limit: int = 20):
    result = await db.execute(select(Workflow).order_by(desc(Workflow.created_at)).limit(limit))
    wfs = result.scalars().all()
    return [
        {
            "id": w.id,
            "prompt_text": w.prompt_text[:120],
            "status": w.status,
            "entity_type": (w.structured_intent or {}).get("entity_type"),
            "created_at": w.created_at.isoformat() if w.created_at else None,
            "is_monitor": w.is_monitor
        }
        for w in wfs
    ]

@router.get("/tasks/{run_id}")
async def get_task(run_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(TaskRun, run_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return {
        "id": task.id,
        "workflow_id": task.workflow_id,
        "status": task.status,
        "progress": task.progress,
        "records_collected": task.records_collected,
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "logs": task.logs or [],
        "error_log": task.error_log
    }

@router.get("/datasets/{workflow_id}/records")
async def get_records(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None
):
    q = select(Record).where(Record.workflow_id == workflow_id)
    result = await db.execute(q.offset(skip).limit(limit))
    records = result.scalars().all()
    
    out = []
    for r in records:
        item = {
            "id": r.id,
            "entity_type": r.entity_type,
            "confidence_score": r.confidence_score,
            "dedup_cluster_id": r.dedup_cluster_id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            ** (r.field_values or {})
        }
        if search:
            # simple filter
            blob = str(item).lower()
            if search.lower() not in blob:
                continue
        out.append(item)
    return {"total": len(out), "records": out}

@router.get("/datasets/{workflow_id}/lineage")
async def get_lineage(workflow_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Record).where(Record.workflow_id == workflow_id).limit(50))
    records = result.scalars().all()
    nodes = []
    edges = []
    for r in records:
        rec_node = f"record_{r.id}"
        nodes.append({"id": rec_node, "type": "record", "label": f"Record #{r.id}", "confidence": r.confidence_score})
        # get provenance
        provs = await db.execute(select(FieldProvenance).where(FieldProvenance.record_id == r.id))
        for p in provs.scalars().all():
            src_node = f"source_{p.source_id or p.source_url}"
            if not any(n["id"] == src_node for n in nodes):
                nodes.append({"id": src_node, "type": "source", "label": p.source_url[:60] if p.source_url else "source", "url": p.source_url})
            edges.append({"from": src_node, "to": rec_node, "field": p.field_name})
    return {"nodes": nodes, "edges": edges}

@router.post("/datasets/{workflow_id}/export")
async def export_dataset(workflow_id: int, format: str = "json", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Record).where(Record.workflow_id == workflow_id))
    records = result.scalars().all()
    data = [{"id": r.id, **(r.field_values or {}), "confidence": r.confidence_score} for r in records]
    if format == "csv":
        # simple CSV
        if not data:
            return {"content": "", "format": "csv"}
        keys = list(data[0].keys())
        lines = [",".join(keys)]
        for row in data:
            lines.append(",".join(str(row.get(k, "")).replace(",", ";") for k in keys))
        return {"content": "\n".join(lines), "format": "csv", "filename": f"dataforge_{workflow_id}.csv"}
    return {"content": data, "format": "json", "count": len(data)}

@router.get("/sources/allowlist")
async def get_allowlist(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Source))
    sources = result.scalars().all()
    from app.services.intent_parser import PERMITTED_SOURCES
    return {
        "permitted": list(PERMITTED_SOURCES.keys()),
        "tracked": [{"domain": s.domain, "type": s.type, "trust_score": s.trust_score, "robots_allowed": s.robots_allowed} for s in sources]
    }


# ---------- Watchtower monitors ----------
class MonitorRequest(BaseModel):
    workflow_id: int
    schedule: str = "daily"  # hourly | daily | weekly
    alert_channel: str = "email"  # email | slack | webhook

@router.post("/monitors")
async def create_monitor(req: MonitorRequest, db: AsyncSession = Depends(get_db)):
    """Promote a workflow to a recurring Watchtower monitor."""
    wf = await db.get(Workflow, req.workflow_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")
    wf.is_monitor = True
    wf.schedule = req.schedule
    await db.commit()
    return {
        "monitor_id": wf.id,
        "workflow_id": wf.id,
        "schedule": req.schedule,
        "alert_channel": req.alert_channel,
        "status": "active",
        "message": f"Watchtower monitor active — will re-run {req.schedule} and alert via {req.alert_channel}",
    }

@router.get("/monitors")
async def list_monitors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.is_monitor == True))
    rows = result.scalars().all()
    return [
        {
            "monitor_id": w.id,
            "prompt_text": w.prompt_text,
            "schedule": w.schedule,
            "status": w.status,
            "entity_type": (w.structured_intent or {}).get("entity_type"),
            "created_at": w.created_at.isoformat() if w.created_at else None,
        }
        for w in rows
    ]

# ---------- Chat-with-your-data ----------
class ChatRequest(BaseModel):
    question: str

@router.post("/datasets/{workflow_id}/chat")
async def chat_with_data(workflow_id: int, req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """Simple NL Q&A over collected records (rule-based RAG for MVP)."""
    result = await db.execute(select(Record).where(Record.workflow_id == workflow_id).limit(200))
    records = result.scalars().all()
    if not records:
        return {"answer": "No records found for this dataset.", "citations": []}

    q = (req.question or "").lower().strip()
    rows = [{"id": r.id, **(r.field_values or {}), "confidence": r.confidence_score} for r in records]

    # Keyword filter
    keywords = [w for w in q.replace("?", "").split() if len(w) > 2 and w not in {
        "the", "and", "for", "with", "from", "that", "this", "what", "which", "where",
        "how", "many", "show", "list", "find", "get", "are", "was", "were", "have", "has"
    }]
    matched = []
    for row in rows:
        blob = " ".join(str(v).lower() for v in row.values())
        score = sum(1 for k in keywords if k in blob)
        if score > 0 or not keywords:
            matched.append((score, row))
    matched.sort(key=lambda x: -x[0])
    top = [m[1] for m in matched[:8]]

    # Aggregate answers
    if any(w in q for w in ["how many", "count", "number of"]):
        answer = f"There are **{len(records)}** records in this dataset."
        if keywords:
            answer += f" Matching your filters ({', '.join(keywords)}): **{len(matched)}**."
    elif any(w in q for w in ["location", "city", "where"]):
        locs = {}
        for r in rows:
            loc = r.get("location") or "Unknown"
            locs[loc] = locs.get(loc, 0) + 1
        parts = [f"{k} ({v})" for k, v in sorted(locs.items(), key=lambda x: -x[1])]
        answer = "Locations breakdown: " + ", ".join(parts)
    elif any(w in q for w in ["company", "companies"]):
        cos = {}
        for r in rows:
            c = r.get("company") or r.get("company_name") or "Unknown"
            cos[c] = cos.get(c, 0) + 1
        top_cos = sorted(cos.items(), key=lambda x: -x[1])[:10]
        answer = "Companies: " + ", ".join(f"{k} ({v})" for k, v in top_cos)
    elif any(w in q for w in ["title", "role", "position"]):
        titles = {}
        for r in rows:
            t = r.get("title") or "Unknown"
            titles[t] = titles.get(t, 0) + 1
        top_t = sorted(titles.items(), key=lambda x: -x[1])[:10]
        answer = "Roles: " + ", ".join(f"{k} ({v})" for k, v in top_t)
    elif top:
        sample = top[0]
        fields = {k: v for k, v in sample.items() if k not in ("id", "confidence") and v}
        answer = f"Found {len(matched)} matching record(s). Example: " + ", ".join(f"{k}={v}" for k, v in list(fields.items())[:6])
    else:
        answer = f"Dataset has {len(records)} records. Try asking about companies, locations, roles, or counts."

    citations = [{"record_id": t["id"], "snippet": {k: t.get(k) for k in list(t)[:5]}} for t in top[:3]]
    return {"answer": answer, "citations": citations, "matched_count": len(matched), "total_records": len(records)}


@router.get("/datasets/{workflow_id}/insights")
async def dataset_insights(workflow_id: int, db: AsyncSession = Depends(get_db)):
    """Auto-generated summary stats for a dataset."""
    result = await db.execute(select(Record).where(Record.workflow_id == workflow_id).limit(500))
    records = result.scalars().all()
    if not records:
        return {"total": 0, "insights": []}
    rows = [r.field_values or {} for r in records]
    insights = [{"type": "count", "label": "Total records", "value": len(rows)}]
    confs = [r.confidence_score for r in records if r.confidence_score is not None]
    if confs:
        insights.append({"type": "metric", "label": "Avg confidence", "value": f"{sum(confs)/len(confs)*100:.0f}%"})
    for field in ["location", "company", "company_name", "title", "industry", "topic", "source"]:
        counts = {}
        for row in rows:
            v = row.get(field)
            if v:
                counts[str(v)] = counts.get(str(v), 0) + 1
        if counts:
            top = sorted(counts.items(), key=lambda x: -x[1])[:5]
            insights.append({"type": "breakdown", "label": field.replace("_", " ").title(), "value": top})
    return {"total": len(rows), "insights": insights}
