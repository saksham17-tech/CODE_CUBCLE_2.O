"""
DataForge AI — Intent Parser & Workflow Planner
Accurate NL → structured intent for diverse business data needs.
"""
from typing import Dict, Any, Optional, List
import re
import uuid
from datetime import datetime

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
    "careers360.com": {"type": "scrape", "trust": 0.85, "category": "education"},
    "shiksha.com": {"type": "scrape", "trust": 0.85, "category": "education"},
    "ndtv.com": {"type": "scrape", "trust": 0.88, "category": "news"},
    "economictimes.indiatimes.com": {"type": "scrape", "trust": 0.9, "category": "news"},
}

LOCATION_MAP = {
    "bengaluru": "Bengaluru", "bangalore": "Bengaluru", "blr": "Bengaluru",
    "mumbai": "Mumbai", "bombay": "Mumbai",
    "delhi": "Delhi", "new delhi": "Delhi", "ncr": "Delhi NCR",
    "hyderabad": "Hyderabad", "hyd": "Hyderabad",
    "chennai": "Chennai", "madras": "Chennai",
    "pune": "Pune",
    "kolkata": "Kolkata", "calcutta": "Kolkata",
    "gurgaon": "Gurgaon", "gurugram": "Gurgaon",
    "noida": "Noida",
    "ahmedabad": "Ahmedabad", "jaipur": "Jaipur",
    "chandigarh": "Chandigarh", "kochi": "Kochi", "coimbatore": "Coimbatore",
    "indore": "Indore", "lucknow": "Lucknow", "bhubaneswar": "Bhubaneswar",
    "india": "India", "remote": "Remote", "work from home": "Remote", "wfh": "Remote",
}

JOB_TITLE_PATTERNS = [
    (r"data\s*scien(?:ce|tist)", "Data Scientist"),
    (r"data\s*analyst", "Data Analyst"),
    (r"data\s*engineer", "Data Engineer"),
    (r"business\s*analyst", "Business Analyst"),
    (r"backend\s*engineer|back[\-\s]?end\s*(?:engineer|developer)", "Backend Engineer"),
    (r"frontend\s*engineer|front[\-\s]?end\s*(?:engineer|developer)", "Frontend Engineer"),
    (r"full[\s\-]?stack\s*(?:engineer|developer)", "Full Stack Engineer"),
    (r"software\s*(?:engineer|developer)", "Software Engineer"),
    (r"ml\s*engineer|machine\s*learning\s*engineer", "ML Engineer"),
    (r"ai\s*engineer|artificial\s*intelligence\s*engineer", "AI Engineer"),
    (r"devops\s*engineer", "DevOps Engineer"),
    (r"sre|site\s*reliability", "SRE"),
    (r"product\s*manager|\bpm\b", "Product Manager"),
    (r"project\s*manager", "Project Manager"),
    (r"analytics\s*engineer", "Analytics Engineer"),
    (r"platform\s*engineer", "Platform Engineer"),
    (r"cloud\s*engineer", "Cloud Engineer"),
    (r"security\s*engineer|cyber\s*security", "Security Engineer"),
    (r"qa\s*engineer|test\s*engineer|sdet", "QA Engineer"),
    (r"android\s*(?:developer|engineer)", "Android Engineer"),
    (r"ios\s*(?:developer|engineer)", "iOS Engineer"),
    (r"ui\s*/?\s*ux\s*designer|product\s*designer", "UI/UX Designer"),
    (r"hr\s*manager|human\s*resources", "HR Manager"),
    (r"sales\s*manager|account\s*executive", "Sales Manager"),
    (r"marketing\s*manager|growth\s*manager", "Marketing Manager"),
    (r"content\s*writer|technical\s*writer", "Content Writer"),
    (r"chartered\s*accountant|\bca\b", "Chartered Accountant"),
    (r"nurse|nursing", "Nurse"),
    (r"teacher|faculty|professor", "Teacher"),
]

INDUSTRY_MAP = {
    "saas": "SaaS", "fintech": "Fintech", "edtech": "EdTech", "healthtech": "HealthTech",
    "ecommerce": "E-commerce", "e-commerce": "E-commerce", "logistics": "Logistics",
    "gaming": "Gaming", "crypto": "Crypto", "blockchain": "Blockchain",
    "telecom": "Telecom", "automotive": "Automotive", "manufacturing": "Manufacturing",
    "banking": "Banking", "insurance": "Insurance", "consulting": "Consulting",
    "it services": "IT Services", "media": "Media", "travel": "Travel",
}

TOPIC_MAP = {
    "jee": "JEE", "jev": "JEE", "neet": "NEET", "upsc": "UPSC", "gate": "GATE",
    "cat exam": "CAT", "cat ": "CAT", "board exam": "Board Exams",
    "fintech": "Fintech", "saas": "SaaS", "startup": "Startups", "startups": "Startups",
    "ai": "AI", "artificial intelligence": "AI", "machine learning": "AI",
    "cricket": "Cricket", "bollywood": "Bollywood", "tech": "Technology",
    "education": "Education", "exam": "Exams", "climate": "Climate",
    "stock market": "Stock Market", "ipo": "IPO", "crypto": "Crypto",
}

def _extract_location(text: str) -> Optional[str]:
    for key in sorted(LOCATION_MAP.keys(), key=len, reverse=True):
        if re.search(rf"\b{re.escape(key)}\b", text):
            return LOCATION_MAP[key]
    return None

def _extract_job_title(text: str) -> Optional[str]:
    for pattern, title in JOB_TITLE_PATTERNS:
        if re.search(pattern, text, re.I):
            return title
    return None

def _extract_industry(text: str) -> Optional[str]:
    for key, label in sorted(INDUSTRY_MAP.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(key)}\b", text):
            return label
    return None

def _extract_topic(text: str) -> Optional[str]:
    for key, label in sorted(TOPIC_MAP.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(key)}\b", text):
            return label
    return None

def _extract_limit(text: str) -> int:
    for pat in [
        r"\b(\d{1,3})\s+most\b",
        r"\b(?:top|first|latest|recent|all)\s+(\d{1,3})\b",
        r"\bfind\s+(?:me\s+)?(\d{1,3})\b",
        r"\b(\d{1,3})\s*(?:mid[\-\s]?size\s+)?(?:companies|jobs|leads|openings|records|results|saas|startups|articles|posts|blogs|products|events)?\b",
    ]:
        m = re.search(pat, text)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 100:
                return n
    if re.search(r"\ball\b", text):
        return 25
    return 15

def _extract_seniority(text: str) -> Optional[str]:
    if re.search(r"\bintern\b|\binternship\b", text):
        return "Intern"
    if re.search(r"\bjunior\b|\bentry[\-\s]?level\b|\bfresher\b", text):
        return "Junior"
    if re.search(r"\bprincipal\b", text):
        return "Principal"
    if re.search(r"\bstaff\b", text):
        return "Staff"
    if re.search(r"\blead\b", text):
        return "Lead"
    if re.search(r"\bsenior\b|\bsr\.?\b", text):
        return "Senior"
    return None

def parse_intent(prompt: str) -> Dict[str, Any]:
    prompt_lower = prompt.lower().strip()
    entity_type = "generic"
    required_fields = ["name", "url", "description"]
    filters: Dict[str, Any] = {}
    preferred_sources: List[str] = ["web_search"]

    location = _extract_location(prompt_lower)
    industry = _extract_industry(prompt_lower)
    topic = _extract_topic(prompt_lower)
    limit = _extract_limit(prompt_lower)

    # --- JOBS ---
    job_signals = ["job", "opening", "hiring", "position", "role", "vacancy", "recruit",
                   "openings for", "jobs for", "career", "careers", "vacancy"]
    if any(k in prompt_lower for k in job_signals) or _extract_job_title(prompt_lower):
        # Prefer jobs if title pattern matched even without explicit "job"
        if any(k in prompt_lower for k in job_signals) or (
            _extract_job_title(prompt_lower) and not any(k in prompt_lower for k in ["article", "news", "blog", "viral"])
        ):
            entity_type = "job_opening"
            required_fields = ["title", "company", "location", "posted_date", "url", "description", "salary"]
            preferred_sources = ["indeed.com", "naukri.com", "linkedin.com", "glassdoor.com"]
            if location:
                filters["location"] = location
            title = _extract_job_title(prompt_lower)
            if title:
                filters["title_contains"] = title
            seniority = _extract_seniority(prompt_lower)
            if seniority:
                filters["seniority"] = seniority
            if industry:
                filters["industry"] = industry
            if any(x in prompt_lower for x in ["this week", "posted this week", "last 7 days", "past week"]):
                filters["posted_within_days"] = 7
            elif any(x in prompt_lower for x in ["this month", "last 30 days", "past month"]):
                filters["posted_within_days"] = 30
            if re.search(r"remote|wfh|work from home", prompt_lower):
                filters["location"] = "Remote"

    # --- COMPANY / LEADS ---
    if entity_type == "generic" and not any(k in prompt_lower for k in ["sponsor", "sponsorship", "conference", "summit"]) and any(k in prompt_lower for k in [
        "company", "companies", "saas", "startup", "startups", "lead", "leads",
        "prospect", "funding", "raised", "investor", "series a", "series b"
    ]):
        entity_type = "company_lead"
        required_fields = ["company_name", "industry", "location", "funding_stage", "website", "email", "founder_linkedin"]
        preferred_sources = ["crunchbase.com", "angel.co", "ycombinator.com", "linkedin.com", "web_search"]
        if location:
            filters["location"] = location
        if industry:
            filters["industry"] = industry
        if any(x in prompt_lower for x in ["mid-size", "mid size", "midsize"]):
            filters["size"] = "mid-size"
        if any(x in prompt_lower for x in ["funding", "raised", "series"]):
            filters["has_funding"] = True
            if "6 months" in prompt_lower or "last 6" in prompt_lower:
                filters["funding_within_months"] = 6
            elif "12 months" in prompt_lower or "last year" in prompt_lower or "past year" in prompt_lower:
                filters["funding_within_months"] = 12

    # --- SPONSORS / EVENTS ---
    if entity_type == "generic" and any(k in prompt_lower for k in [
        "sponsor", "sponsorship", "conference", "event", "summit", "meetup", "partnership"
    ]):
        entity_type = "sponsor_prospect"
        required_fields = ["company_name", "event_name", "year", "contact", "website", "industry", "location"]
        preferred_sources = ["web_search", "linkedin.com"]
        if industry:
            filters["industry"] = industry.lower()
        if location:
            filters["location"] = location

    # --- ARTICLES / NEWS ---
    if entity_type == "generic" and any(k in prompt_lower for k in [
        "article", "articles", "news", "blog", "viral", "trending", "headline", "post", "posts"
    ]):
        entity_type = "article"
        required_fields = ["title", "source", "url", "published_date", "summary", "topic", "engagement"]
        preferred_sources = ["web_search", "rss", "ndtv.com", "economictimes.indiatimes.com"]
        if topic:
            filters["topic"] = topic
        if "viral" in prompt_lower or "trending" in prompt_lower:
            filters["sort"] = "viral"
        if "recent" in prompt_lower or "latest" in prompt_lower:
            filters["sort"] = filters.get("sort") or "recent"

    # --- PRODUCTS ---
    if entity_type == "generic" and any(k in prompt_lower for k in [
        "product hunt", "producthunt", "products", "tools", "software tools", "apps"
    ]):
        entity_type = "product"
        required_fields = ["name", "tagline", "url", "category", "upvotes", "pricing"]
        preferred_sources = ["producthunt.com", "web_search"]
        if industry or topic:
            filters["category"] = industry or topic

    # --- PRICING / COMPETITOR ---
    if entity_type == "generic" and any(k in prompt_lower for k in [
        "pricing", "competitor", "competitors", "price", "compare price"
    ]):
        entity_type = "pricing_page"
        required_fields = ["product_name", "plan", "price", "currency", "url", "last_checked"]
        preferred_sources = ["web_search"]

    # --- GITHUB / OPEN SOURCE ---
    if entity_type == "generic" and any(k in prompt_lower for k in [
        "github", "open source", "repository", "repos", "libraries"
    ]):
        entity_type = "github_repo"
        required_fields = ["name", "description", "url", "stars", "language", "topics"]
        preferred_sources = ["github.com"]
        if topic:
            filters["topic"] = topic

    # residual location
    if location and "location" not in filters:
        filters["location"] = location

    return {
        "original_prompt": prompt,
        "entity_type": entity_type,
        "required_fields": required_fields,
        "filters": filters,
        "preferred_sources": preferred_sources,
        "limit": limit,
        "output_schema": {f: "string" for f in required_fields},
        "confidence": 0.93 if entity_type != "generic" else 0.6,
        "parsed_at": datetime.utcnow().isoformat(),
    }

def generate_workflow_dag(intent: Dict[str, Any]) -> Dict[str, Any]:
    nodes, edges = [], []
    search_node = {
        "id": "node_search", "type": "search", "label": "Discover Sources",
        "description": f"Search permitted sources for {intent['entity_type']}",
        "config": {"query": intent["original_prompt"], "sources": intent["preferred_sources"], "limit": intent.get("limit", 15)},
        "status": "pending", "estimated_time_sec": 1,
    }
    nodes.append(search_node)
    extract_nodes = []
    for i, src in enumerate(intent["preferred_sources"][:4]):
        nid = f"node_extract_{i}"
        extract_nodes.append({
            "id": nid, "type": "extract", "label": f"Extract from {src}",
            "description": f"Parse fields from {src}",
            "config": {"source": src, "fields": intent["required_fields"],
                       "method": PERMITTED_SOURCES.get(src, {}).get("type", "scrape")},
            "status": "pending", "estimated_time_sec": 1,
        })
        edges.append({"from": "node_search", "to": nid})
    nodes.extend(extract_nodes)
    for nid, label, desc, sec in [
        ("node_validate", "Validate & Score", "Schema + confidence + PII checks", 1),
        ("node_dedup", "Deduplicate", "Near-duplicate merge across sources", 1),
        ("node_store", "Store + Lineage", "Persist with full provenance", 1),
    ]:
        nodes.append({"id": nid, "type": nid.replace("node_", ""), "label": label, "description": desc,
                      "config": {}, "status": "pending", "estimated_time_sec": sec})
    for n in extract_nodes:
        edges.append({"from": n["id"], "to": "node_validate"})
    edges += [{"from": "node_validate", "to": "node_dedup"}, {"from": "node_dedup", "to": "node_store"}]
    total = sum(n.get("estimated_time_sec", 1) for n in nodes)
    return {
        "id": str(uuid.uuid4())[:8], "version": 1, "nodes": nodes, "edges": edges,
        "estimated_total_sec": total, "estimated_records": intent.get("limit", 15),
        "compliance_note": "Allowlist + robots.txt enforced before any request",
        "created_at": datetime.utcnow().isoformat(),
    }

def estimate_cost_time(dag: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "estimated_seconds": dag.get("estimated_total_sec", 8),
        "estimated_records": dag.get("estimated_records", 15),
        "estimated_cost_usd": round(0.01 + (dag.get("estimated_records", 15) * 0.0005), 3),
        "sandbox_available": True,
    }
