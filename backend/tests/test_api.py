"""Smoke tests for the portfolio API: seeding, public reads, admin 401, CRUD."""

import os

os.environ["ADMIN_KEY"] = "test-key"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
KEY = {"X-Admin-Key": "test-key"}


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_seeded_projects():
    r = client.get("/api/projects")
    assert r.status_code == 200
    projects = r.json()
    assert len(projects) == 9
    assert projects[0]["title"] == "IncidentPilot"
    assert "5/5" in projects[0]["measured"]
    assert projects[1]["title"] == "RegLens"
    assert "0.897" in projects[1]["measured"]


def test_profile():
    r = client.get("/api/profile")
    assert r.status_code == 200
    assert r.json()["name"] == "Gautam Keshri"
    assert "7.62" in r.json()["education"]


def test_skills():
    r = client.get("/api/skills")
    assert r.status_code == 200
    assert any(g["category"] == "Generative AI" for g in r.json())


def test_admin_requires_key():
    assert client.post("/api/projects", json={"title": "Nope"}).status_code == 401
    assert client.put("/api/profile", json={"name": "Nope"}).status_code == 401
    assert client.put("/api/skills", json={"groups": []}).status_code == 401
    assert client.delete("/api/projects/1").status_code == 401


def test_project_crud_with_key():
    r = client.post(
        "/api/projects",
        json={"title": "Temp Project", "description": "to delete", "stack": ["Python"]},
        headers=KEY,
    )
    assert r.status_code == 201
    pid = r.json()["id"]
    r = client.put(
        f"/api/projects/{pid}",
        json={"title": "Temp Project 2", "description": "edited", "stack": ["Python"]},
        headers=KEY,
    )
    assert r.status_code == 200 and r.json()["title"] == "Temp Project 2"
    r = client.delete(f"/api/projects/{pid}", headers=KEY)
    assert r.status_code == 200
    assert all(p["id"] != pid for p in client.get("/api/projects").json())
