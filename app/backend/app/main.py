from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.ollama_client import OllamaClient
from app.schemas import HealthResponse, TriageRequest, TriageResponse
from app.services.triage import create_triage_response

app = FastAPI(
    title="Gemma SUS Assistant API",
    version="0.1.0",
    description="Local-first API shell for SUS-oriented structured guidance.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model_runtime="ollama_enabled" if settings.use_ollama else "mock",
        rag_index="not_configured",
    )


@app.post("/api/triage", response_model=TriageResponse)
async def triage(request: TriageRequest) -> TriageResponse:
    settings = get_settings()
    runtime = None
    if settings.use_ollama:
        runtime = OllamaClient(
            settings.ollama_base_url,
            settings.ollama_model,
            settings.ollama_timeout_seconds,
        )

    return await create_triage_response(request.case_text, runtime)
