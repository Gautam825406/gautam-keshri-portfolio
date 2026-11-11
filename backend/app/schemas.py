"""Pydantic schemas for the portfolio API."""

from pydantic import BaseModel, Field


class ProfileIn(BaseModel):
    name: str = ""
    title: str = ""
    summary: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""
    location: str = ""
    education: str = ""
    certification: str = ""


class ProfileOut(ProfileIn):
    id: int = 1


class ProjectIn(BaseModel):
    title: str
    description: str = ""
    measured: str = ""
    live_url: str = ""
    github_url: str = ""
    stack: list[str] = Field(default_factory=list)
    sort_order: int = 0


class ProjectOut(ProjectIn):
    id: int


class SkillGroup(BaseModel):
    category: str
    items: list[str] = Field(default_factory=list)


class SkillsIn(BaseModel):
    groups: list[SkillGroup] = Field(default_factory=list)
