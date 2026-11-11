"""Admin protection: a single ADMIN_KEY from the environment.

Admin endpoints require header ``X-Admin-Key`` matching ADMIN_KEY.
Default (dev only) is "change-me" — set a strong key in .env / hosting
env vars before deploying. Public GET endpoints need no key.
"""

import os

from fastapi import Header, HTTPException


def get_admin_key() -> str:
    return os.environ.get("ADMIN_KEY", "change-me")


def require_admin(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")):
    if x_admin_key is None or x_admin_key != get_admin_key():
        raise HTTPException(status_code=401, detail="Invalid or missing X-Admin-Key")
    return True
