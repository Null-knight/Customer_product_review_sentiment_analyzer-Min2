from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import admin, analytics, products, reviews, users
from src.api.websocket.live_stream import review_stream
from src.utils.config import PROJECT_ROOT
from src.utils.memory_monitor import memory_snapshot

app = FastAPI(title="Customer Product Review Sentiment Analyzer", version="0.1.0")
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "src" / "dashboard" / "templates"), name="static")
app.include_router(reviews.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(analytics.router)
app.websocket("/ws/reviews")(review_stream)


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(
        PROJECT_ROOT
        / "src"
        / "dashboard"
        / "templates"
        / "index.html"
    )


@app.get("/analytics")
def analytics_dashboard() -> FileResponse:
    return FileResponse(
        PROJECT_ROOT
        / "src"
        / "dashboard"
        / "templates"
        / "analytics.html"
    )


@app.get("/admin")
def admin_dashboard() -> FileResponse:
    return FileResponse(
        PROJECT_ROOT
        / "src"
        / "dashboard"
        / "templates"
        / "admin.html"
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "memory": memory_snapshot()}