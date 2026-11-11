import os

import uvicorn

if __name__ == "__main__":
    # Hosts (Render etc.) assign the port via $PORT; default 8000 locally.
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
