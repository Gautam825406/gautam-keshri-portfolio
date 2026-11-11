"""SQLAlchemy models. Stacks are stored as JSON text to keep SQLite simple."""

import json

from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    title = Column(String, default="")
    summary = Column(Text, default="")
    email = Column(String, default="")
    linkedin = Column(String, default="")
    github = Column(String, default="")
    location = Column(String, default="")
    education = Column(String, default="")
    certification = Column(String, default="")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    measured = Column(Text, default="")  # measured eval line, or "" if none
    live_url = Column(String, default="")
    github_url = Column(String, default="")
    stack_json = Column(Text, default="[]")
    sort_order = Column(Integer, default=0)

    @property
    def stack(self):
        try:
            return json.loads(self.stack_json or "[]")
        except json.JSONDecodeError:
            return []

    @stack.setter
    def stack(self, value):
        self.stack_json = json.dumps(list(value or []))


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)
