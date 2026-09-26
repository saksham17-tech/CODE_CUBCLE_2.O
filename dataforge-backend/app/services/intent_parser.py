"""
Intent Parser & Workflow Planner for DataForge AI.
In production this uses Claude/LLM. For MVP we use a robust rule + template system
that produces realistic structured intents and editable DAGs for common business use-cases.
"""
from typing import Dict, Any, List, Optional
import re
import uuid
from datetime import datetime

# Allowed sources (compliance by design)
PERMITTED_SOURCES = {
    "linkedin.com": {"type": "scrape", "trust": 0.85, "category": "professional"},
    "indeed.com": {"type": "scrape", "trust": 0.9, "category": "jobs"},
    "naukri.com": {"type": "scrape", "trust": 0.88, "category": "jobs"},
    "glassdoor.com": {"type": "scrape", "trust": 0.82, "category": "jobs"},
    "crunchbase.com": {"type": "scrape", "trust": 0.9, "category": "funding"},
    "angel.co": {"type": "scrape", "trust": 0.8, "category": "startups"},
    "ycombinator.com": {"type": "scrape", "trust": 0.95, "category": "startups"},
    "news.ycombinator.com": {"type": "scrape", "trust": 0.9, "category": "tech"},
    "github.com": {"type": "api", "trust": 0.95, "category": "tech"},
    "producthunt.com": {"type": "scrape", "trust": 0.85, "category": "products"},
    "rss": {"type": "rss", "trust": 0.9, "category": "feeds"},
    "web_search": {"type": "search", "trust": 0.75, "category": "general"},
}

def parse_intent(prompt: str) -> Dict[str, Any]:
    """Convert natural language prompt into structured intent."""
    prompt_lower = prompt.lower().strip()
    
    # Detect entity type
    entity_type = "generic"
    required_fields = ["name", "url", "description"]
    filters = {}
    preferred_sources = ["web_search"]
    output_schema = {}
    
    # Job-related
    if any(k in prompt_lower for k in ["job", "opening", "hiring", "position", "role", "vacancy", "recruit"]):
        entity_type = "job_opening"
        required_fields = ["title", "company", "location", "posted_date", "url", "description", "salary"]
        preferred_sources = ["indeed.com", "naukri.com", "linkedin.com", "glassdoor.com"]
        if "bengaluru" in prompt_lower or "bangalore" in prompt_lower:
            filters["location"] = "Bengaluru"
        if "senior" in prompt_lower:
            filters["seniority"] = "Senior"
        if "data engineer" in prompt_lower:
            filters["title_contains"] = "Data Engineer"
        if "this week" in prompt_lower or "posted this week" in prompt_lower:
            filters["posted_within_days"] = 7
            
    # Company / Lead / SaaS
    elif any(k in prompt_lower for k in ["company", "saas", "startup", "lead", "prospect", "funding", "raised"]):
        entity_type = "company_lead"
        required_fields = ["company_name", "industry", "location", "funding_stage", "founder_linkedin", "website", "email"]
        preferred_sources = ["crunchbase.com", "angel.co", "ycombinator.com", "linkedin.com", "web_search"]
        if "india" in prompt_lower:
            filters["location"] = "India"
        if "saas" in prompt_lower:
            filters["industry"] = "SaaS"
        if "mid-size" in prompt_lower or "mid size" in prompt_lower:
            filters["size"] = "mid-size"
        if "funding" in prompt_lower or "raised" in prompt_lower:
            filters["has_funding"] = True
            if "6 months" in prompt_lower or "last 6" in prompt_lower:
                filters["funding_within_months"] = 6
                
    # Sponsor / Event
    elif any(k in prompt_lower for k in ["sponsor", "sponsorship", "conference", "event", "partnership"]):
        entity_type = "sponsor_prospect"
        required_fields = ["company_name", "event_name", "year", "contact", "website", "industry"]
        preferred_sources = ["web_search", "linkedin.com"]
        if "fintech" in prompt_lower:
            filters["industry"] = "fintech"
            
    # Pricing / Competitor
    elif any(k in prompt_lower for k in ["pricing", "competitor", "price", "track"]):
        entity_type = "pricing_page"
        required_fields = ["product_name", "plan", "price", "currency", "url", "last_checked"]
        preferred_sources = ["web_search"]
        
    # Extract numbers
    num_match = re.search(r"(\d+)\s*(companies|jobs|leads|openings|records|results)", prompt_lower)
    limit = int(num_match.group(1)) if num_match else 20
    if limit > 100:
        limit = 100
        
    structured = {
        "original_prompt": prompt,
        "entity_type": entity_type,
        "required_fields": required_fields,
        "filters": filters,
        "preferred_sources": preferred_sources,
        "limit": limit,
        "output_schema": {f: "string" for f in required_fields},
        "confidence": 0.92,
        "parsed_at": datetime.utcnow().isoformat()
    }
    return structured

def generate_workflow_dag(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Generate an editable visual DAG plan from structured intent."""
    nodes = []
    edges = []
    
    # 1. Search / Discover node
    search_node = {
        "id": "node_search",
        "type": "search",
        "label": "Discover Sources",
        "description": f"Search for relevant {intent['entity_type']} pages using permitted sources",
        "config": {
            "query": intent["original_prompt"],
            "sources": intent["preferred_sources"],
            "limit": intent.get("limit", 20)
        },
        "status": "pending",
        "estimated_time_sec": 15
    }
    nodes.append(search_node)
    
    # 2. Extract nodes per source type
    extract_nodes = []
    for i, src in enumerate(intent["preferred_sources"][:4]):
        node_id = f"node_extract_{i}"
        extract_nodes.append({
            "id": node_id,
            "type": "extract",
            "label": f"Extract from {src}",
            "description": f"Scrape/parse structured fields from {src}",
            "config": {
                "source": src,
                "fields": intent["required_fields"],
                "method": PERMITTED_SOURCES.get(src, {}).get("type", "scrape")
            },
            "status": "pending",
            "estimated_time_sec": 30
        })
        edges.append({"from": "node_search", "to": node_id})
    nodes.extend(extract_nodes)
    
    # 3. Validate
    validate_node = {
        "id": "node_validate",
        "type": "validate",
        "label": "Validate & Score",
        "description": "Rule + confidence scoring, schema mapping, PII check",
        "config": {
            "schema": intent["output_schema"],
            "min_confidence": 0.6
        },
        "status": "pending",
        "estimated_time_sec": 10
    }
    nodes.append(validate_node)
    for n in extract_nodes:
        edges.append({"from": n["id"], "to": "node_validate"})
    
    # 4. Dedup
    dedup_node = {
        "id": "node_dedup",
        "type": "dedup",
        "label": "Deduplicate & Resolve",
        "description": "Embedding-based near-duplicate merge across sources",
        "config": {"similarity_threshold": 0.85},
        "status": "pending",
        "estimated_time_sec": 8
    }
    nodes.append(dedup_node)
    edges.append({"from": "node_validate", "to": "node_dedup"})
    
    # 5. Store
    store_node = {
        "id": "node_store",
        "type": "store",
        "label": "Store + Lineage",
        "description": "Persist records with full provenance and trust scores",
        "config": {},
        "status": "pending",
        "estimated_time_sec": 5
    }
    nodes.append(store_node)
    edges.append({"from": "node_dedup", "to": "node_store"})
    
    total_est = sum(n.get("estimated_time_sec", 10) for n in nodes)
    
    dag = {
        "id": str(uuid.uuid4())[:8],
        "version": 1,
        "nodes": nodes,
        "edges": edges,
        "estimated_total_sec": total_est,
        "estimated_records": intent.get("limit", 20),
        "compliance_note": "All sources checked against allowlist + robots.txt before execution",
        "created_at": datetime.utcnow().isoformat()
    }
    return dag

def estimate_cost_time(dag: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "estimated_seconds": dag.get("estimated_total_sec", 60),
        "estimated_records": dag.get("estimated_records", 20),
        "estimated_cost_usd": round(0.02 + (dag.get("estimated_records", 20) * 0.001), 3),
        "sandbox_available": True
    }
