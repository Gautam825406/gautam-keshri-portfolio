"""Seed the DB on first run (only if empty). Verified facts only —
no invented metrics, dates, jobs or salaries."""

from sqlalchemy.orm import Session

from .models import Profile, Project, Skill

PROFILE = {
    "name": "Gautam Keshri",
    "title": "Generative AI Engineer | AI Engineer Intern",
    "summary": (
        "Designs, evaluates and deploys production AI systems — multi-agent "
        "LangGraph workflows, citation-grounded RAG and text-to-SQL agents, "
        "measured LLM evaluations, guardrails and abstention, automated "
        "testing and live deployments. Seeking AI Engineer / Generative AI "
        "Intern roles."
    ),
    "email": "keshrigautam825406@gmail.com",
    "linkedin": "https://www.linkedin.com/in/gautam-keshri/",
    "github": "https://github.com/Gautam825406",
    "location": "Bengaluru, India",
    "education": (
        "B.Sc. (Hons.) Data Science and Artificial Intelligence, "
        "IIT Guwahati, expected June 2027, CGPA 7.62/10"
    ),
    "certification": "IBM Data Science Professional Certificate (Coursera)",
}

# (title, description, measured, live_url, github_url, stack)
PROJECTS = [
    (
        "IncidentPilot",
        "Multi-Agent Production Incident Resolver. LangGraph supervisor "
        "orchestrates Triage, Logs, Metrics and Knowledge agents; "
        "evidence-linked hypotheses; human approval before remediation.",
        "Measured (live, Groq openai/gpt-oss-120b, n=6, 11 Nov 2026): "
        "semantic top-1 5/5, abstention 1/1, evidence 1.0, unsafe 0; "
        "220 backend tests pass.",
        "https://incidentpilot-ten.vercel.app/",
        "https://github.com/Gautam825406/incidentpilot",
        ["Python", "FastAPI", "LangGraph", "Groq", "PostgreSQL", "React", "TypeScript", "Docker"],
    ),
    (
        "RegLens",
        "Grounded GraphRAG for Contracts & Compliance. Citation-grounded "
        "answers from a knowledge graph, honest abstention, conflict "
        "detection, obligation register, evidence packs.",
        "Measured (48 cases, 11 Nov 2026): recall@5 0.897, faithfulness "
        "0.974, correct abstention 9/9; 13 backend tests pass.",
        "https://reglens-chi.vercel.app/",
        "https://github.com/Gautam825406/reglens",
        ["Python", "FastAPI", "GraphRAG", "Hybrid Retrieval", "PostgreSQL", "React", "TypeScript", "Docker"],
    ),
    (
        "QueryPilot",
        "Trusted Text-to-SQL Analytics Agent. LangGraph planner, sqlglot "
        "validation (SELECT-only, schema, PII, limits), self-correction "
        "max 3 attempts.",
        "Measured (50 cases, 11 Nov 2026): execution accuracy 100% "
        "(50/50), safety 11/11 blocked; 56 backend tests pass.",
        "https://querypilot-chi.vercel.app/",
        "https://github.com/Gautam825406/querypilot",
        ["Python", "FastAPI", "LangGraph", "sqlglot", "DuckDB", "PostgreSQL", "React"],
    ),
    (
        "CodeSentry",
        "Agentic Secure Code Review + Codebase RAG. AST-aware (tree-sitter) "
        "indexing + call-graph retrieval, evidence-cited CWE/OWASP findings, "
        "validated patches, CI merge gating.",
        "",
        "https://codesentry-one.vercel.app/",
        "https://github.com/Gautam825406/codesentry",
        ["Python", "FastAPI", "LangGraph", "tree-sitter", "GitHub Checks"],
    ),
    (
        "U++ Academy",
        "Live Tuition & Coaching Platform (Classes 6-12). Role-based "
        "dashboards, batches, lectures, tests with server-side scoring, "
        "fees/receipts, Cashfree pay-and-enrol for real students.",
        "",
        "https://u-academy-zeta.vercel.app/",
        "https://github.com/Gautam825406/u-academy",
        ["Next.js", "TypeScript", "Supabase", "PostgreSQL", "Cashfree"],
    ),
    (
        "ContentForge AI",
        "LangGraph blog generation — topics/transcripts to structured articles.",
        "",
        "",
        "https://github.com/Gautam825406/ContentForge-AI",
        ["Python", "FastAPI", "LangGraph", "LangChain", "Pydantic", "React", "Pytest"],
    ),
    (
        "ResearchMind",
        "Multi-stage web research agent (Tavily tool calling).",
        "",
        "",
        "https://github.com/Gautam825406/ResearchMind",
        ["Python", "FastAPI", "LangChain", "Groq", "Tavily", "BeautifulSoup", "React", "Pytest"],
    ),
    (
        "ResumeForge AI",
        "ATS resume optimisation, 7-factor matching, structured outputs, "
        "PDF/DOCX export.",
        "",
        "",
        "https://github.com/Gautam825406/ResumeForge-AI",
        ["Python", "FastAPI", "LangChain", "OpenAI", "React", "TypeScript", "Docker"],
    ),
    (
        "PDF RAG Chatbot",
        "FAISS semantic search over PDFs.",
        "",
        "",
        "https://github.com/Gautam825406/document_Analysis_using_AI",
        ["Python", "FastAPI", "Streamlit", "Sentence Transformers", "FAISS", "Groq", "PyMuPDF"],
    ),
]

SKILLS = [
    ("Programming", ["Python", "SQL", "JavaScript", "TypeScript", "C++"]),
    ("Generative AI", ["LangChain", "LangGraph", "LLMs", "Prompt Engineering", "Structured Outputs", "Tool Calling", "Agentic Workflows"]),
    ("RAG & Retrieval", ["RAG", "GraphRAG", "Embeddings", "Sentence Transformers", "FAISS", "Hybrid Retrieval", "Document Chunking"]),
    ("Backend & Data", ["FastAPI", "REST APIs", "Pydantic", "PostgreSQL", "Supabase", "Docker"]),
    ("ML & Testing", ["Scikit-learn", "Pandas", "NumPy", "LLM Evaluation", "Pytest"]),
]


def seed_if_empty(db: Session) -> None:
    if db.query(Profile).first() is not None:
        return
    db.add(Profile(id=1, **PROFILE))
    for i, (title, description, measured, live_url, github_url, stack) in enumerate(PROJECTS):
        p = Project(
            title=title,
            description=description,
            measured=measured,
            live_url=live_url,
            github_url=github_url,
            sort_order=i,
        )
        p.stack = stack
        db.add(p)
    order = 0
    for category, items in SKILLS:
        for item in items:
            db.add(Skill(category=category, name=item, sort_order=order))
            order += 1
    db.commit()
