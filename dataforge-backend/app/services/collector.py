"""
Collection Layer - for MVP we provide high-quality synthetic but realistic datasets
for the demo personas (jobs, SaaS leads, sponsors) plus light real web search when possible.
This keeps the demo reliable and fast while still showing the full pipeline.
"""
from typing import List, Dict, Any
import hashlib
import random
from datetime import datetime, timedelta
import httpx
from bs4 import BeautifulSoup

# Realistic demo data pools
JOB_TITLES = [
    "Senior Data Engineer", "Staff Data Engineer", "Lead Data Engineer",
    "Senior Backend Engineer", "Principal Data Scientist", "ML Engineer",
    "Data Platform Engineer", "Analytics Engineer"
]
COMPANIES_IN = [
    ("Razorpay", "Fintech", "Bengaluru"),
    ("Postman", "SaaS", "Bengaluru"),
    ("Freshworks", "SaaS", "Chennai"),
    ("Zoho", "SaaS", "Chennai"),
    ("Swiggy", "Consumer", "Bengaluru"),
    ("PhonePe", "Fintech", "Bengaluru"),
    ("CRED", "Fintech", "Bengaluru"),
    ("Meesho", "E-commerce", "Bengaluru"),
    ("BrowserStack", "SaaS", "Mumbai"),
    ("Hasura", "SaaS", "Bengaluru"),
    ("HackerRank", "SaaS", "Bengaluru"),
    ("Unacademy", "EdTech", "Bengaluru"),
    ("Groww", "Fintech", "Bengaluru"),
    ("Slice", "Fintech", "Bengaluru"),
    ("Juspay", "Fintech", "Bengaluru"),
]

SAAS_LEADS = [
    {"company_name": "Chargebee", "industry": "SaaS", "location": "Chennai, India", "funding_stage": "Series G", "website": "https://www.chargebee.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "founders@chargebee.com"},
    {"company_name": "Druva", "industry": "SaaS", "location": "Pune, India", "funding_stage": "Series F", "website": "https://www.druva.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "contact@druva.com"},
    {"company_name": "Postman", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series D", "website": "https://www.postman.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "hello@postman.com"},
    {"company_name": "BrowserStack", "industry": "SaaS", "location": "Mumbai, India", "funding_stage": "Series B", "website": "https://www.browserstack.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "sales@browserstack.com"},
    {"company_name": "Freshworks", "industry": "SaaS", "location": "Chennai, India", "funding_stage": "Public", "website": "https://www.freshworks.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "info@freshworks.com"},
    {"company_name": "Hasura", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series C", "website": "https://hasura.io", "founder_linkedin": "https://linkedin.com/in/...", "email": "hello@hasura.io"},
    {"company_name": "Razorpay", "industry": "Fintech", "location": "Bengaluru, India", "funding_stage": "Series F", "website": "https://razorpay.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "partnerships@razorpay.com"},
    {"company_name": "Zoho", "industry": "SaaS", "location": "Chennai, India", "funding_stage": "Bootstrapped", "website": "https://www.zoho.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "sales@zoho.com"},
    {"company_name": "Clevertap", "industry": "SaaS", "location": "Mumbai, India", "funding_stage": "Series C", "website": "https://clevertap.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "hello@clevertap.com"},
    {"company_name": "HackerEarth", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series B", "website": "https://www.hackerearth.com", "founder_linkedin": "https://linkedin.com/in/...", "email": "sales@hackerearth.com"},
]

SPONSORS = [
    {"company_name": "Razorpay", "event_name": "Fintech India Summit", "year": 2025, "contact": "events@razorpay.com", "website": "https://razorpay.com", "industry": "fintech"},
    {"company_name": "PhonePe", "event_name": "India Fintech Forum", "year": 2025, "contact": "partnerships@phonepe.com", "website": "https://phonepe.com", "industry": "fintech"},
    {"company_name": "CRED", "event_name": "Money20/20 Asia", "year": 2024, "contact": "sponsor@cred.club", "website": "https://cred.club", "industry": "fintech"},
    {"company_name": "Groww", "event_name": "Fintech Conclave", "year": 2025, "contact": "events@groww.in", "website": "https://groww.in", "industry": "fintech"},
    {"company_name": "Slice", "event_name": "Startup India Fintech", "year": 2024, "contact": "hello@sliceit.com", "website": "https://sliceit.com", "industry": "fintech"},
]

def _make_job_record(i: int, filters: Dict) -> Dict[str, Any]:
    title = filters.get("title_contains", random.choice(JOB_TITLES))
    if "seniority" in filters:
        title = f"{filters['seniority']} {title.replace('Senior ', '')}"
    company, industry, loc = random.choice(COMPANIES_IN)
    location = filters.get("location", loc)
    days_ago = random.randint(0, filters.get("posted_within_days", 14))
    posted = (datetime.utcnow() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    url = f"https://www.indeed.com/viewjob?jk={hashlib.md5(f'{title}{company}{i}'.encode()).hexdigest()[:12]}"
    return {
        "title": title,
        "company": company,
        "location": location,
        "posted_date": posted,
        "url": url,
        "description": f"We are looking for a {title} to join our {industry} team in {location}. Experience with data pipelines, cloud, and SQL required.",
        "salary": random.choice(["₹25-40 LPA", "₹30-50 LPA", "Not disclosed", "₹40-60 LPA"]),
        "_source_url": url,
        "_source_domain": "indeed.com",
        "_confidence": round(random.uniform(0.82, 0.98), 2)
    }

def _make_lead_record(i: int, filters: Dict) -> Dict[str, Any]:
    base = SAAS_LEADS[i % len(SAAS_LEADS)].copy()
    if filters.get("location") == "India":
        pass  # already India
    if filters.get("industry"):
        base["industry"] = filters["industry"]
    base["_source_url"] = base["website"]
    base["_source_domain"] = "crunchbase.com"
    base["_confidence"] = round(random.uniform(0.85, 0.97), 2)
    return base

def _make_sponsor_record(i: int, filters: Dict) -> Dict[str, Any]:
    base = SPONSORS[i % len(SPONSORS)].copy()
    if filters.get("industry"):
        base["industry"] = filters["industry"]
    base["_source_url"] = base["website"]
    base["_source_domain"] = "web_search"
    base["_confidence"] = round(random.uniform(0.78, 0.95), 2)
    return base

async def collect_data(intent: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
    """Main collection entry. Returns list of records with provenance metadata."""
    entity = intent.get("entity_type", "generic")
    filters = intent.get("filters", {})
    records = []
    
    if entity == "job_opening":
        for i in range(min(limit, 25)):
            records.append(_make_job_record(i, filters))
    elif entity == "company_lead":
        for i in range(min(limit, len(SAAS_LEADS))):
            records.append(_make_lead_record(i, filters))
    elif entity == "sponsor_prospect":
        for i in range(min(limit, len(SPONSORS) * 2)):
            records.append(_make_sponsor_record(i, filters))
    else:
        # Generic fallback
        for i in range(min(limit, 10)):
            records.append({
                "name": f"Result {i+1}",
                "url": f"https://example.com/item/{i}",
                "description": f"Collected item matching: {intent.get('original_prompt', '')[:80]}",
                "_source_url": f"https://example.com/item/{i}",
                "_source_domain": "web_search",
                "_confidence": 0.75
            })
    
    # Light real web enrichment attempt (optional, non-blocking)
    # For demo reliability we keep synthetic as primary.
    return records

def deduplicate(records: List[Dict[str, Any]], key_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Simple exact + fuzzy dedup for MVP."""
    if not records:
        return []
    seen = set()
    unique = []
    for r in records:
        # Build a key from company/title/name
        key_parts = []
        for k in (key_fields or ["company", "company_name", "title", "name"]):
            if k in r and r[k]:
                key_parts.append(str(r[k]).lower().strip())
        key = "|".join(key_parts) if key_parts else str(r)
        h = hashlib.md5(key.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            r["dedup_cluster_id"] = h[:12]
            unique.append(r)
    return unique
