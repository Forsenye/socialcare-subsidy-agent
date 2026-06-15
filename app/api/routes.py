from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter

from app.agent.classifier import classify_case
from app.agent.handoff import build_handoff_summary
from app.agent.orchestrator import SocialCareAgent
from app.api.schemas import ChatRequest, ClassifyRequest, HandoffRequest, HealthResponse
from app.core.audit import write_audit_event
from app.core.config import get_settings

router = APIRouter()
agent = SocialCareAgent()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name, environment=settings.environment)


@router.post("/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    result = agent.answer(request.message)
    classification = result["classification"]
    write_audit_event(
        category=str(classification["category"]),
        risk_level=str(classification["risk_level"]),
        user_message=request.message,
        response_summary=str(result["response"])[:260],
        escalation_required=bool(result["escalation_required"]),
    )
    return result


@router.post("/classify")
def classify(request: ClassifyRequest) -> dict[str, str]:
    return asdict(classify_case(request.message))


@router.post("/handoff")
def handoff(request: HandoffRequest) -> dict[str, object]:
    classification = classify_case(request.message)
    return build_handoff_summary(request.message, classification)
