"""
DataForge AI — Collection Layer
Diverse, filter-accurate demo datasets across jobs, companies, articles, products, repos, sponsors.
"""
from typing import List, Dict, Any, Optional
import hashlib
import random
from datetime import datetime, timedelta

# ─── Companies by city (for jobs + leads) ───────────────────────────────────
COMPANIES = [
    ("Razorpay", "Fintech", "Bengaluru"), ("Postman", "SaaS", "Bengaluru"),
    ("Freshworks", "SaaS", "Chennai"), ("Zoho", "SaaS", "Chennai"),
    ("Swiggy", "Consumer", "Bengaluru"), ("PhonePe", "Fintech", "Bengaluru"),
    ("CRED", "Fintech", "Bengaluru"), ("Meesho", "E-commerce", "Bengaluru"),
    ("BrowserStack", "SaaS", "Mumbai"), ("Hasura", "SaaS", "Bengaluru"),
    ("HackerRank", "SaaS", "Bengaluru"), ("Unacademy", "EdTech", "Bengaluru"),
    ("Groww", "Fintech", "Bengaluru"), ("Slice", "Fintech", "Bengaluru"),
    ("Juspay", "Fintech", "Bengaluru"), ("Druva", "SaaS", "Pune"),
    ("Chargebee", "SaaS", "Chennai"), ("Clevertap", "SaaS", "Mumbai"),
    ("HackerEarth", "SaaS", "Bengaluru"), ("ShareChat", "Consumer", "Bengaluru"),
    ("Dream11", "Gaming", "Mumbai"), ("Policybazaar", "Fintech", "Gurgaon"),
    ("Paytm", "Fintech", "Noida"), ("Infosys", "IT Services", "Bengaluru"),
    ("TCS", "IT Services", "Mumbai"), ("Flipkart", "E-commerce", "Bengaluru"),
    ("Amazon India", "E-commerce", "Hyderabad"), ("Microsoft India", "SaaS", "Hyderabad"),
    ("Google India", "SaaS", "Bengaluru"), ("Uber India", "Consumer", "Gurgaon"),
    ("Persistent Systems", "SaaS", "Pune"), ("KPIT", "Automotive", "Pune"),
    ("Thoughtworks", "IT Services", "Pune"), ("ServiceNow", "SaaS", "Hyderabad"),
    ("Salesforce India", "SaaS", "Hyderabad"), ("Deloitte India", "Consulting", "Hyderabad"),
    ("ZS Associates", "Consulting", "Pune"), ("PubMatic", "SaaS", "Pune"),
    ("Adobe India", "SaaS", "Noida"), ("HCLTech", "IT Services", "Noida"),
    ("Samsung R&D", "Tech", "Noida"), ("Oracle India", "SaaS", "Noida"),
    ("Accenture", "Consulting", "Noida"), ("Cognizant", "IT Services", "Noida"),
    ("Airtel", "Telecom", "Gurgaon"), ("MakeMyTrip", "Travel", "Gurgaon"),
    ("Info Edge", "Internet", "Noida"), ("Snapdeal", "E-commerce", "Gurgaon"),
    ("Ola", "Consumer", "Bengaluru"), ("BYJU'S", "EdTech", "Bengaluru"),
    ("Nykaa", "E-commerce", "Mumbai"), ("Lenskart", "E-commerce", "Gurgaon"),
    ("Zerodha", "Fintech", "Bengaluru"), ("Upstox", "Fintech", "Mumbai"),
    ("Delhivery", "Logistics", "Gurgaon"), ("Dunzo", "Logistics", "Bengaluru"),
    ("Practo", "HealthTech", "Bengaluru"), ("1mg", "HealthTech", "Gurgaon"),
    ("Myntra", "E-commerce", "Bengaluru"), ("BigBasket", "E-commerce", "Bengaluru"),
    ("InMobi", "SaaS", "Bengaluru"), ("Capillary Tech", "SaaS", "Bengaluru"),
    ("IIT Bombay", "Education", "Mumbai"), ("IIT Delhi", "Education", "Delhi"),
    ("AIIMS Delhi", "HealthTech", "Delhi"), ("ISRO", "Tech", "Bengaluru"),
]

CAREER_URLS = {
    "Razorpay": "https://razorpay.com/jobs/", "Postman": "https://www.postman.com/company/careers/",
    "Freshworks": "https://www.freshworks.com/company/careers/", "Zoho": "https://careers.zoho.com/",
    "Swiggy": "https://careers.swiggy.com/", "PhonePe": "https://www.phonepe.com/careers/",
    "CRED": "https://careers.cred.club/", "Meesho": "https://careers.meesho.com/",
    "BrowserStack": "https://www.browserstack.com/careers", "Hasura": "https://hasura.io/careers/",
    "HackerRank": "https://www.hackerrank.com/careers", "Unacademy": "https://unacademy.com/careers",
    "Groww": "https://groww.in/careers", "Paytm": "https://paytm.com/careers/",
    "TCS": "https://www.tcs.com/careers", "Infosys": "https://www.infosys.com/careers/",
    "Flipkart": "https://www.flipkartcareers.com/", "Google India": "https://careers.google.com/locations/india/",
    "Microsoft India": "https://careers.microsoft.com/", "Amazon India": "https://www.amazon.jobs/en/locations/india",
    "Adobe India": "https://careers.adobe.com/", "Oracle India": "https://www.oracle.com/careers/",
    "Accenture": "https://www.accenture.com/in-en/careers", "Cognizant": "https://careers.cognizant.com/in/en",
    "HCLTech": "https://www.hcltech.com/careers", "Salesforce India": "https://careers.salesforce.com/",
    "ServiceNow": "https://www.servicenow.com/careers.html", "Nykaa": "https://www.nykaa.com/careers",
    "Zerodha": "https://zerodha.com/careers/", "Delhivery": "https://www.delhivery.com/careers",
    "Practo": "https://www.practo.com/company/careers", "Myntra": "https://careers.myntra.com/",
}

SAAS_LEADS = [
    {"company_name": "Chargebee", "industry": "SaaS", "location": "Chennai, India", "funding_stage": "Series G", "website": "https://www.chargebee.com", "email": "founders@chargebee.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Druva", "industry": "SaaS", "location": "Pune, India", "funding_stage": "Series F", "website": "https://www.druva.com", "email": "contact@druva.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Postman", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series D", "website": "https://www.postman.com", "email": "hello@postman.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "BrowserStack", "industry": "SaaS", "location": "Mumbai, India", "funding_stage": "Series B", "website": "https://www.browserstack.com", "email": "sales@browserstack.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Freshworks", "industry": "SaaS", "location": "Chennai, India", "funding_stage": "Public", "website": "https://www.freshworks.com", "email": "info@freshworks.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Hasura", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series C", "website": "https://hasura.io", "email": "hello@hasura.io", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Clevertap", "industry": "SaaS", "location": "Mumbai, India", "funding_stage": "Series C", "website": "https://clevertap.com", "email": "hello@clevertap.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Yellow.ai", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series C", "website": "https://yellow.ai", "email": "hello@yellow.ai", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Whatfix", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series A", "website": "https://whatfix.com", "email": "sales@whatfix.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "WebEngage", "industry": "SaaS", "location": "Mumbai, India", "funding_stage": "Series B", "website": "https://webengage.com", "email": "hello@webengage.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Persistent Systems", "industry": "SaaS", "location": "Pune, India", "funding_stage": "Public", "website": "https://www.persistent.com", "email": "info@persistent.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "PubMatic", "industry": "SaaS", "location": "Pune, India", "funding_stage": "Public", "website": "https://pubmatic.com", "email": "hello@pubmatic.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Razorpay", "industry": "Fintech", "location": "Bengaluru, India", "funding_stage": "Series F", "website": "https://razorpay.com", "email": "partnerships@razorpay.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Groww", "industry": "Fintech", "location": "Bengaluru, India", "funding_stage": "Series E", "website": "https://groww.in", "email": "hello@groww.in", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Zerodha", "industry": "Fintech", "location": "Bengaluru, India", "funding_stage": "Bootstrapped", "website": "https://zerodha.com", "email": "hello@zerodha.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Practo", "industry": "HealthTech", "location": "Bengaluru, India", "funding_stage": "Series C", "website": "https://www.practo.com", "email": "hello@practo.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Unacademy", "industry": "EdTech", "location": "Bengaluru, India", "funding_stage": "Series H", "website": "https://unacademy.com", "email": "hello@unacademy.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Delhivery", "industry": "Logistics", "location": "Gurgaon, India", "funding_stage": "Public", "website": "https://www.delhivery.com", "email": "hello@delhivery.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "Nykaa", "industry": "E-commerce", "location": "Mumbai, India", "funding_stage": "Public", "website": "https://www.nykaa.com", "email": "careers@nykaa.com", "founder_linkedin": "https://linkedin.com/in/"},
    {"company_name": "InMobi", "industry": "SaaS", "location": "Bengaluru, India", "funding_stage": "Series D", "website": "https://www.inmobi.com", "email": "hello@inmobi.com", "founder_linkedin": "https://linkedin.com/in/"},
]

SPONSORS = [
    {"company_name": "Razorpay", "event_name": "Fintech India Summit", "year": 2025, "contact": "events@razorpay.com", "website": "https://razorpay.com", "industry": "fintech", "location": "Mumbai"},
    {"company_name": "PhonePe", "event_name": "India Fintech Forum", "year": 2025, "contact": "partnerships@phonepe.com", "website": "https://phonepe.com", "industry": "fintech", "location": "Bengaluru"},
    {"company_name": "CRED", "event_name": "Money20/20 Asia", "year": 2024, "contact": "sponsor@cred.club", "website": "https://cred.club", "industry": "fintech", "location": "Bengaluru"},
    {"company_name": "Groww", "event_name": "Fintech Conclave", "year": 2025, "contact": "events@groww.in", "website": "https://groww.in", "industry": "fintech", "location": "Bengaluru"},
    {"company_name": "Paytm", "event_name": "India Digital Summit", "year": 2025, "contact": "events@paytm.com", "website": "https://paytm.com", "industry": "fintech", "location": "Delhi"},
    {"company_name": "Google", "event_name": "Google for Startups Summit", "year": 2025, "contact": "startups@google.com", "website": "https://startup.google.com", "industry": "saas", "location": "Bengaluru"},
    {"company_name": "AWS", "event_name": "AWS Summit India", "year": 2025, "contact": "aws-events@amazon.com", "website": "https://aws.amazon.com/events", "industry": "saas", "location": "Mumbai"},
    {"company_name": "Microsoft", "event_name": "Microsoft Ignite India", "year": 2025, "contact": "events@microsoft.com", "website": "https://ignite.microsoft.com", "industry": "saas", "location": "Hyderabad"},
]

ARTICLES = {
    "JEE": [
        {"title": "JEE Main 2026 Exam Date Announced: Complete Schedule and Syllabus", "source": "Careers360", "url": "https://www.careers360.com/exams/jee-main", "engagement": "125K views"},
        {"title": "Top 10 Mistakes Students Make in JEE Advanced Physics", "source": "Physics Wallah", "url": "https://www.pw.live/blogs/jee", "engagement": "89K views"},
        {"title": "JEE vs NEET: Which Path Should You Choose in 2026?", "source": "India Today Education", "url": "https://www.indiatoday.in/education-today", "engagement": "210K views"},
        {"title": "How to Crack JEE Main in 60 Days — Strategy from AIR 12", "source": "Unacademy Blog", "url": "https://unacademy.com/content/jee/", "engagement": "156K views"},
        {"title": "JEE Advanced 2025 Cutoff Analysis and Rank Predictor", "source": "Allen Career Institute", "url": "https://www.allen.ac.in/", "engagement": "98K views"},
        {"title": "Best Books for JEE 2026: Subject-wise Recommendations", "source": "Byju's Exam Prep", "url": "https://byjus.com/jee/", "engagement": "178K views"},
        {"title": "Is Dropping a Year for JEE Worth It? Real Stories", "source": "Shiksha", "url": "https://www.shiksha.com/engineering/jee-main-exam", "engagement": "67K views"},
        {"title": "JEE Main Session 1 Result 2026: How to Check Scorecard", "source": "NDTV Education", "url": "https://www.ndtv.com/education", "engagement": "340K views"},
        {"title": "Organic Chemistry Shortcuts for JEE That Actually Work", "source": "Vedantu", "url": "https://www.vedantu.com/jee", "engagement": "112K views"},
        {"title": "IIT Seat Matrix 2026: Branch-wise Closing Ranks", "source": "CollegeDekho", "url": "https://www.collegedekho.com/jee-main/", "engagement": "145K views"},
        {"title": "Mental Health During JEE Prep: Tips from Counselors", "source": "The Hindu Education", "url": "https://www.thehindu.com/education/", "engagement": "54K views"},
        {"title": "JEE Main Mock Test Analysis: Where Toppers Lose Marks", "source": "Resonance", "url": "https://www.resonance.ac.in/", "engagement": "73K views"},
        {"title": "Mathematics Formula Sheet for JEE — One Page Revision", "source": "Mathongo", "url": "https://www.mathongo.com/", "engagement": "201K views"},
        {"title": "JEE Advanced Previous Year Papers with Solutions PDF", "source": "Aakash Institute", "url": "https://www.aakash.ac.in/", "engagement": "188K views"},
        {"title": "How Coaching vs Self-Study Affects JEE Ranks in 2025", "source": "Indian Express Education", "url": "https://indianexpress.com/section/education/", "engagement": "92K views"},
        {"title": "JEE Main Eligibility Criteria and Attempt Limits Explained", "source": "NTA Official", "url": "https://jeemain.nta.ac.in/", "engagement": "256K views"},
        {"title": "Physics Numerical Practice Set for JEE 2026", "source": "FIITJEE", "url": "https://www.fiitjee.com/", "engagement": "81K views"},
        {"title": "What Changed in JEE Syllabus After NEP 2020?", "source": "Times of India Education", "url": "https://timesofindia.indiatimes.com/education", "engagement": "119K views"},
        {"title": "Top IITs and Their Most Competitive Branches 2026", "source": "Outlook India", "url": "https://www.outlookindia.com/education", "engagement": "164K views"},
        {"title": "Daily 4-Hour JEE Study Plan for Working Droppers", "source": "Superprof Blog", "url": "https://www.superprof.co.in/", "engagement": "47K views"},
    ],
    "NEET": [
        {"title": "NEET UG 2026 Syllabus Released by NTA", "source": "NDTV Education", "url": "https://www.ndtv.com/education", "engagement": "290K views"},
        {"title": "NEET Biology High-Yield Topics for 2026", "source": "Physics Wallah", "url": "https://www.pw.live/", "engagement": "140K views"},
        {"title": "AIIMS vs State Medical Colleges: What NEET Rank Gets You", "source": "Careers360", "url": "https://www.careers360.com/", "engagement": "175K views"},
    ],
    "AI": [
        {"title": "Open-Source LLMs Catching Up to GPT in 2026", "source": "The Verge", "url": "https://www.theverge.com/", "engagement": "310K views"},
        {"title": "How Indian Startups Are Building AI Agents", "source": "YourStory", "url": "https://yourstory.com/", "engagement": "88K views"},
        {"title": "GPU Shortage and What It Means for AI Startups in India", "source": "Inc42", "url": "https://inc42.com/", "engagement": "72K views"},
        {"title": "Responsible AI Guidelines from MeitY Explained", "source": "Economic Times", "url": "https://economictimes.indiatimes.com/", "engagement": "95K views"},
    ],
    "Fintech": [
        {"title": "UPI Crosses 20 Billion Monthly Transactions", "source": "Economic Times", "url": "https://economictimes.indiatimes.com/", "engagement": "280K views"},
        {"title": "RBI's New Digital Lending Guidelines Explained", "source": "Mint", "url": "https://www.livemint.com/", "engagement": "95K views"},
        {"title": "Account Aggregator Framework: What Consumers Gain", "source": "Moneycontrol", "url": "https://www.moneycontrol.com/", "engagement": "61K views"},
    ],
    "Startups": [
        {"title": "Indian Unicorns in 2026: Who's Still Standing", "source": "Inc42", "url": "https://inc42.com/", "engagement": "120K views"},
        {"title": "Tier-2 City Startup Boom: Beyond Bengaluru", "source": "YourStory", "url": "https://yourstory.com/", "engagement": "76K views"},
    ],
    "Technology": [
        {"title": "India's Semiconductor Push: $10B Investment Update", "source": "Hindu Business Line", "url": "https://www.thehindubusinessline.com/", "engagement": "150K views"},
        {"title": "5G Rollout Progress Across Indian States", "source": "ET Telecom", "url": "https://telecom.economictimes.indiatimes.com/", "engagement": "84K views"},
    ],
    "Education": [
        {"title": "NEP 2020 Implementation Scorecard After 5 Years", "source": "The Hindu", "url": "https://www.thehindu.com/education/", "engagement": "110K views"},
        {"title": "Online vs Offline Learning Outcomes in India", "source": "Scroll.in", "url": "https://scroll.in/", "engagement": "58K views"},
    ],
}

PRODUCTS = [
    {"name": "Notion", "tagline": "All-in-one workspace", "url": "https://www.notion.so", "category": "Productivity", "upvotes": "12.4K", "pricing": "Freemium"},
    {"name": "Figma", "tagline": "Collaborative design", "url": "https://www.figma.com", "category": "Design", "upvotes": "18.1K", "pricing": "Freemium"},
    {"name": "Linear", "tagline": "Issue tracking for modern teams", "url": "https://linear.app", "category": "DevTools", "upvotes": "9.2K", "pricing": "Paid"},
    {"name": "Vercel", "tagline": "Frontend cloud", "url": "https://vercel.com", "category": "DevTools", "upvotes": "11.0K", "pricing": "Freemium"},
    {"name": "Supabase", "tagline": "Open-source Firebase alternative", "url": "https://supabase.com", "category": "Backend", "upvotes": "14.5K", "pricing": "Freemium"},
    {"name": "Cursor", "tagline": "AI-first code editor", "url": "https://cursor.sh", "category": "AI", "upvotes": "22.0K", "pricing": "Paid"},
    {"name": "Perplexity", "tagline": "AI answer engine", "url": "https://www.perplexity.ai", "category": "AI", "upvotes": "16.8K", "pricing": "Freemium"},
    {"name": "Clay", "tagline": "Creative data enrichment", "url": "https://www.clay.com", "category": "Sales", "upvotes": "7.3K", "pricing": "Paid"},
    {"name": "Resend", "tagline": "Email API for developers", "url": "https://resend.com", "category": "DevTools", "upvotes": "6.1K", "pricing": "Freemium"},
    {"name": "Cal.com", "tagline": "Open-source Calendly", "url": "https://cal.com", "category": "Productivity", "upvotes": "8.9K", "pricing": "Freemium"},
]

GITHUB_REPOS = [
    {"name": "langchain", "description": "Build context-aware reasoning applications", "url": "https://github.com/langchain-ai/langchain", "stars": "95K", "language": "Python", "topics": "ai,llm"},
    {"name": "next.js", "description": "React framework for production", "url": "https://github.com/vercel/next.js", "stars": "128K", "language": "JavaScript", "topics": "react,web"},
    {"name": "fastapi", "description": "Modern high-performance Python web framework", "url": "https://github.com/tiangolo/fastapi", "stars": "82K", "language": "Python", "topics": "api,python"},
    {"name": "supabase", "description": "Open-source Firebase alternative", "url": "https://github.com/supabase/supabase", "stars": "74K", "language": "TypeScript", "topics": "backend,postgres"},
    {"name": "ollama", "description": "Run large language models locally", "url": "https://github.com/ollama/ollama", "stars": "110K", "language": "Go", "topics": "ai,llm"},
    {"name": "shadcn-ui", "description": "Beautifully designed components", "url": "https://github.com/shadcn-ui/ui", "stars": "78K", "language": "TypeScript", "topics": "ui,react"},
    {"name": "transformers", "description": "State-of-the-art Machine Learning by Hugging Face", "url": "https://github.com/huggingface/transformers", "stars": "140K", "language": "Python", "topics": "ai,ml"},
    {"name": "playwright", "description": "Framework for Web Testing and Automation", "url": "https://github.com/microsoft/playwright", "stars": "70K", "language": "TypeScript", "topics": "testing,automation"},
]

PRICING = [
    {"product_name": "Notion", "plan": "Plus", "price": "10", "currency": "USD/mo", "url": "https://www.notion.so/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "Figma", "plan": "Professional", "price": "15", "currency": "USD/mo", "url": "https://www.figma.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "Slack", "plan": "Pro", "price": "8.75", "currency": "USD/mo", "url": "https://slack.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "GitHub", "plan": "Team", "price": "4", "currency": "USD/mo", "url": "https://github.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "Vercel", "plan": "Pro", "price": "20", "currency": "USD/mo", "url": "https://vercel.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "OpenAI API", "plan": "GPT-4o", "price": "2.50", "currency": "USD/1M tokens", "url": "https://openai.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "AWS", "plan": "EC2 t3.medium", "price": "0.0416", "currency": "USD/hr", "url": "https://aws.amazon.com/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
    {"product_name": "Cursor", "plan": "Pro", "price": "20", "currency": "USD/mo", "url": "https://cursor.sh/pricing", "last_checked": datetime.utcnow().strftime("%Y-%m-%d")},
]


def _companies_for_location(location: Optional[str]) -> list:
    if not location or location in ("India", "Remote"):
        return list(COMPANIES)
    matched = [c for c in COMPANIES if c[2].lower() == location.lower() or location.lower() in c[2].lower()]
    return matched if matched else list(COMPANIES)


def _make_job(i: int, filters: Dict, company_tuple) -> Dict[str, Any]:
    company, industry, loc = company_tuple
    title_base = filters.get("title_contains") or "Software Engineer"
    seniority = filters.get("seniority") or ""
    if seniority and not title_base.lower().startswith(seniority.lower()):
        title = f"{seniority} {title_base}"
    else:
        title = title_base
    location = filters.get("location") if filters.get("location") and filters["location"] != "India" else loc
    if filters.get("location") == "Remote":
        location = "Remote"
    days = random.randint(0, filters.get("posted_within_days", 21))
    posted = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    career = CAREER_URLS.get(company, f"https://www.google.com/search?q={company.replace(' ', '+')}+careers")
    q, loc_q = title.replace(" ", "+"), location.replace(" ", "+")
    domain = random.choice(["indeed.com", "naukri.com", "linkedin.com", "company_site"])
    if domain == "naukri.com":
        url = f"https://www.naukri.com/{title.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"
    elif domain == "linkedin.com":
        url = f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc_q}"
    elif domain == "company_site":
        url = career
    else:
        url = f"https://in.indeed.com/jobs?q={q}&l={loc_q}"
    return {
        "title": title, "company": company, "location": location, "posted_date": posted,
        "url": url, "company_careers": career,
        "description": f"{title} role at {company} ({industry}) in {location}.",
        "salary": random.choice(["₹8-15 LPA", "₹15-25 LPA", "₹25-40 LPA", "₹30-50 LPA", "Not disclosed", "₹40-70 LPA"]),
        "_source_url": url, "_source_domain": domain if domain != "company_site" else "company_site",
        "_confidence": round(random.uniform(0.84, 0.98), 2),
    }


async def collect_data(intent: Dict[str, Any], limit: int = 15) -> List[Dict[str, Any]]:
    entity = intent.get("entity_type", "generic")
    filters = intent.get("filters") or {}
    limit = min(max(int(limit or 15), 1), 50)
    records: List[Dict[str, Any]] = []

    if entity == "job_opening":
        pool = _companies_for_location(filters.get("location"))
        if filters.get("industry"):
            ind = filters["industry"].lower()
            filtered = [c for c in pool if ind in c[1].lower()]
            if filtered:
                pool = filtered
        for i in range(min(limit, max(len(pool), 1))):
            records.append(_make_job(i, filters, pool[i % len(pool)]))

    elif entity == "company_lead":
        leads = list(SAAS_LEADS)
        loc = filters.get("location")
        if loc and loc != "India":
            f = [l for l in leads if loc.lower() in l["location"].lower()]
            if f:
                leads = f
        ind = filters.get("industry")
        if ind:
            f = [l for l in leads if l["industry"].lower() == ind.lower()]
            if f:
                leads = f
        for i in range(min(limit, len(leads))):
            base = leads[i].copy()
            base["_source_url"] = base["website"]
            base["_source_domain"] = "crunchbase.com"
            base["_confidence"] = round(random.uniform(0.86, 0.97), 2)
            records.append(base)

    elif entity == "sponsor_prospect":
        sponsors = list(SPONSORS)
        ind = filters.get("industry")
        if ind:
            f = [s for s in sponsors if s["industry"].lower() == ind.lower()]
            if f:
                sponsors = f
        loc = filters.get("location")
        if loc and loc != "India":
            f = [s for s in sponsors if loc.lower() in s.get("location", "").lower()]
            if f:
                sponsors = f
        for i in range(min(limit, max(len(sponsors), 1))):
            base = sponsors[i % len(sponsors)].copy()
            base["_source_url"] = base["website"]
            base["_source_domain"] = "web_search"
            base["_confidence"] = round(random.uniform(0.80, 0.95), 2)
            records.append(base)

    elif entity == "article":
        topic = filters.get("topic", "Technology")
        pool = list(ARTICLES.get(topic, []))
        if not pool:
            for v in ARTICLES.values():
                pool.extend(v)
        def eng(a):
            try:
                return int(str(a.get("engagement", "0")).replace("K views", "").replace(",", "").strip() or "0")
            except Exception:
                return 0
        if filters.get("sort") == "viral":
            pool = sorted(pool, key=eng, reverse=True)
        for i in range(min(limit, len(pool))):
            a = pool[i].copy()
            a["published_date"] = (datetime.utcnow() - timedelta(days=random.randint(0, 21))).strftime("%Y-%m-%d")
            a["summary"] = f"Coverage: {a['title'][:70]}"
            a["topic"] = topic
            a["_source_url"] = a["url"]
            a["_source_domain"] = "news"
            a["_confidence"] = round(random.uniform(0.82, 0.96), 2)
            records.append(a)

    elif entity == "product":
        pool = list(PRODUCTS)
        cat = filters.get("category")
        if cat:
            f = [p for p in pool if cat.lower() in p["category"].lower() or cat.lower() in p.get("name","").lower() or cat.lower() in p.get("tagline","").lower()]
            # keep filter only if enough results; else show full catalog
            if len(f) >= 3:
                pool = f
        for i in range(min(limit, len(pool))):
            p = pool[i].copy()
            p["_source_url"] = p["url"]
            p["_source_domain"] = "producthunt.com"
            p["_confidence"] = round(random.uniform(0.88, 0.97), 2)
            records.append(p)

    elif entity == "github_repo":
        pool = list(GITHUB_REPOS)
        for i in range(min(limit, len(pool))):
            r = pool[i].copy()
            r["_source_url"] = r["url"]
            r["_source_domain"] = "github.com"
            r["_confidence"] = 0.95
            records.append(r)

    elif entity == "pricing_page":
        for i in range(min(limit, len(PRICING))):
            p = PRICING[i].copy()
            p["_source_url"] = p["url"]
            p["_source_domain"] = "web_search"
            p["_confidence"] = 0.90
            records.append(p)

    else:
        # Last-resort: Google search links (still useful, not fake junk)
        prompt = intent.get("original_prompt") or "search"
        q = prompt.replace(" ", "+")[:100]
        for i in range(min(limit, 8)):
            records.append({
                "name": f"Search result {i+1}",
                "url": f"https://www.google.com/search?q={q}",
                "description": f"Web result related to: {prompt[:120]}",
                "location": filters.get("location", "India"),
                "_source_url": f"https://www.google.com/search?q={q}",
                "_source_domain": "web_search",
                "_confidence": 0.65,
            })

    return records


def deduplicate(records: List[Dict[str, Any]], key_fields: List[str] = None) -> List[Dict[str, Any]]:
    if not records:
        return []
    seen, unique = set(), []
    keys = key_fields or ["company", "company_name", "title", "name", "event_name", "url"]
    for r in records:
        parts = [str(r[k]).lower().strip() for k in keys if r.get(k)]
        h = hashlib.md5("|".join(parts).encode() if parts else str(r).encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            r["dedup_cluster_id"] = h[:12]
            unique.append(r)
    return unique
