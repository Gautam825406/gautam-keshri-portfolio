"""Portfolio API — FastAPI + SQLite. REST only, no frontend code here.

Public (no key):  GET /api/health, /api/profile, /api/projects, /api/skills
Admin (header X-Admin-Key): PUT /api/profile, POST/PUT/DELETE /api/projects,
PUT /api/skills. Wrong or missing key -> 401.
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine, get_db
from .seed import seed_if_empty
from .security import require_admin

Base.metadata.create_all(bind=engine)

# Seed once, on first run, when the DB is empty.
with SessionLocal() as _db:
    seed_if_empty(_db)

app = FastAPI(title="Gautam Keshri Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def profile_out(p: models.Profile) -> schemas.ProfileOut:
    return schemas.ProfileOut(
        id=p.id, name=p.name, title=p.title, summary=p.summary,
        email=p.email, linkedin=p.linkedin, github=p.github,
        location=p.location, education=p.education,
        certification=p.certification,
    )


def project_out(p: models.Project) -> schemas.ProjectOut:
    return schemas.ProjectOut(
        id=p.id, title=p.title, description=p.description,
        measured=p.measured, live_url=p.live_url,
        github_url=p.github_url, stack=p.stack, sort_order=p.sort_order,
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/profile", response_model=schemas.ProfileOut)
def get_profile(db: Session = Depends(get_db)):
    p = db.query(models.Profile).filter(models.Profile.id == 1).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_out(p)


@app.put("/api/profile", response_model=schemas.ProfileOut, dependencies=[Depends(require_admin)])
def update_profile(data: schemas.ProfileIn, db: Session = Depends(get_db)):
    p = db.query(models.Profile).filter(models.Profile.id == 1).first()
    if p is None:
        p = models.Profile(id=1, **data.model_dump())
        db.add(p)
    else:
        for key, value in data.model_dump().items():
            setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return profile_out(p)


@app.get("/api/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    rows = db.query(models.Project).order_by(models.Project.sort_order, models.Project.id).all()
    return [project_out(r) for r in rows]


@app.post("/api/projects", response_model=schemas.ProjectOut, status_code=201, dependencies=[Depends(require_admin)])
def create_project(data: schemas.ProjectIn, db: Session = Depends(get_db)):
    p = models.Project(
        title=data.title, description=data.description, measured=data.measured,
        live_url=data.live_url, github_url=data.github_url,
        sort_order=data.sort_order,
    )
    p.stack = data.stack
    db.add(p)
    db.commit()
    db.refresh(p)
    return project_out(p)


@app.put("/api/projects/{project_id}", response_model=schemas.ProjectOut, dependencies=[Depends(require_admin)])
def update_project(project_id: int, data: schemas.ProjectIn, db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Project not found")
    p.title = data.title
    p.description = data.description
    p.measured = data.measured
    p.live_url = data.live_url
    p.github_url = data.github_url
    p.sort_order = data.sort_order
    p.stack = data.stack
    db.commit()
    db.refresh(p)
    return project_out(p)


@app.delete("/api/projects/{project_id}", dependencies=[Depends(require_admin)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(p)
    db.commit()
    return {"deleted": project_id}


@app.get("/api/skills", response_model=list[schemas.SkillGroup])
def list_skills(db: Session = Depends(get_db)):
    rows = db.query(models.Skill).order_by(models.Skill.sort_order).all()
    groups: dict[str, list[str]] = {}
    for r in rows:
        groups.setdefault(r.category, []).append(r.name)
    return [schemas.SkillGroup(category=k, items=v) for k, v in groups.items()]


@app.put("/api/skills", response_model=list[schemas.SkillGroup], dependencies=[Depends(require_admin)])
def replace_skills(data: schemas.SkillsIn, db: Session = Depends(get_db)):
    db.query(models.Skill).delete()
    order = 0
    for group in data.groups:
        for item in group.items:
            item = item.strip()
            if not item:
                continue
            db.add(models.Skill(category=group.category.strip() or "Other", name=item, sort_order=order))
            order += 1
    db.commit()
    return list_skills(db)
