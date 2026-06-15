from __future__ import annotations

from app.agent.classifier import Classification
from app.agent.safety import mask_sensitive_data


def build_handoff_summary(message: str, classification: Classification) -> dict[str, object]:
    requires_human = (
        classification.risk_level == "high" or classification.category == "sensitive_case"
    )
    masked_need = mask_sensitive_data(message)
    next_step = (
        "Derivar a un asesor humano con prioridad y entregar solo el resumen seguro."
        if requires_human
        else "Continuar con orientación general y validar en canales oficiales."
    )
    return {
        "case_type": classification.category,
        "risk_level": classification.risk_level,
        "user_need": masked_need,
        "safe_summary": (
            f"Usuario solicita orientación sobre {classification.category}. "
            f"Detalle seguro: {masked_need[:280]}"
        ),
        "recommended_next_step": next_step,
        "requires_human_advisor": requires_human,
    }
