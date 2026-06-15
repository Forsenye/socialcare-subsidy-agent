from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter

from app.agent.classifier import classify_case
from app.agent.handoff import build_handoff_summary
from app.agent.orchestrator import SocialCareAgent
from app.agent.safety import mask_sensitive_data
from app.api.schemas import ChatRequest, ClassifyRequest, HandoffRequest, HealthResponse
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
    _write_audit_event(
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


def _write_audit_event(
    category: str,
    risk_level: str,
    user_message: str,
    response_summary: str,
    escalation_required: bool,
) -> None:
    settings = get_settings()
    path = Path(settings.audit_log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "category": category,
        "risk_level": risk_level,
        "user_message_masked": mask_sensitive_data(user_message),
        "response_summary": response_summary,
        "escalation_required": escalation_required,
    }
    with path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(event, ensure_ascii=False) + "\n")
