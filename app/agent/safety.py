from __future__ import annotations

import re

SENSITIVE_PATTERNS = [
    re.compile(r"\b\d{8,12}\b"),
    re.compile(r"\b\d{13,19}\b"),
    re.compile(r"(?i)\b(contraseña|password|clave|pin|token|otp)\b"),
    re.compile(r"(?i)\b(cuenta bancaria|tarjeta de crédito|tarjeta credito|cvv)\b"),
]

UNSAFE_DECISION_PATTERNS = [
    re.compile(r"(?i)\b(aprobado|aprobada|negado|negada|rechazado|rechazada)\b"),
    re.compile(r"(?i)\b(te garantizo|garantizado|beneficio confirmado)\b"),
]


def contains_sensitive_data_request(message: str) -> bool:
    text = message.lower()
    request_terms = ("dime", "envía", "envia", "comparte", "escribe", "ingresa", "manda")
    sensitive_terms = (
        "contraseña",
        "clave",
        "cuenta bancaria",
        "tarjeta",
        "documento completo",
        "cvv",
    )
    return any(term in text for term in request_terms) and any(
        term in text for term in sensitive_terms
    )


def mask_sensitive_data(message: str) -> str:
    masked = message
    for pattern in SENSITIVE_PATTERNS:
        masked = pattern.sub("[DATO_ENMASCARADO]", masked)
    return masked


def response_has_unsafe_decision(response: str) -> bool:
    return any(pattern.search(response) for pattern in UNSAFE_DECISION_PATTERNS)


def enforce_response_boundaries(response: str) -> str:
    boundary = (
        "\n\nLímite importante: esta orientación es simulada, no aprueba ni niega beneficios "
        "y no reemplaza los canales oficiales ni la asesoría de un profesional."
    )
    if "no aprueba ni niega" in response.lower():
        return response
    return f"{response}{boundary}"


def requires_safety_escalation(message: str, risk_level: str) -> bool:
    return risk_level == "high" or contains_sensitive_data_request(message)
