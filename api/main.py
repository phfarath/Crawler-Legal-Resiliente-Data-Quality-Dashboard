"""Aplicação principal da API FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import decisions, health, metrics

app = FastAPI(
    title="Crawler Legal Resiliente API",
    description="API para consulta de decisões judiciais",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(decisions.router, prefix="/api/v1/decisions", tags=["Decisions"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])


@app.get("/")
def root():
    return {"message": "Crawler Legal Resiliente API", "version": "1.0.0"}
