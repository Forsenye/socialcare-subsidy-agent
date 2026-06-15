from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from app.agent.safety import mask_sensitive_data
from app.core.config import get_settings


def write_audit_event(
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
        "response_summary": response_summary[:260],
        "escalation_required": escalation_required,
    }
    with path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(event, ensure_ascii=False) + "\n")
