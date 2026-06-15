from __future__ import annotations

from dataclasses import dataclass

VALID_CATEGORIES = {
    "unemployment_subsidy",
    "child_services",
    "family_support",
    "general_orientation",
    "sensitive_case",
    "out_of_scope",
}

VALID_RISK_LEVELS = {"low", "medium", "high"}


@dataclass(frozen=True)
class Classification:
    category: str
    risk_level: str
    rationale: str


HIGH_RISK_TERMS = {
    "violencia",
    "abuso",
    "amenaza",
    "urgente",
    "emergencia",
    "desalojo",
    "menor",
    "niño solo",
    "maltrato",
    "riesgo",
    "suicidio",
    "hambre",
}

MEDIUM_RISK_TERMS = {
    "documentos",
    "paso a paso",
    "requisitos",
    "radicar",
    "postular",
    "cita",
    "seguimiento",
}

CATEGORY_TERMS = {
    "unemployment_subsidy": {
        "desempleo",
        "cesante",
        "subsidio",
        "sin trabajo",
        "sin empleo",
        "perdí el empleo",
        "perdi el empleo",
        "perdí mi empleo",
        "perdi mi empleo",
        "quedé sin empleo",
        "quede sin empleo",
    },
    "child_services": {
        "niño",
        "niña",
        "menor",
        "jardín",
        "jardin",
        "colegio",
        "infancia",
        "hijo",
        "hija",
    },
    "family_support": {
        "familia",
        "hogar",
        "madre cabeza",
        "apoyo familiar",
        "vivienda",
        "alimentación",
        "alimentacion",
    },
}

OUT_OF_SCOPE_TERMS = {
    "inversión",
    "inversion",
    "criptomoneda",
    "apuesta",
    "trabajo interno",
    "contraseña",
    "hackear",
}


def classify_case(message: str) -> Classification:
    text = message.lower().strip()

    if any(term in text for term in HIGH_RISK_TERMS):
        category = _category_from_text(text) or "sensitive_case"
        return Classification(
            category=category,
            risk_level="high",
            rationale="Caso sensible o urgente.",
        )

    if any(term in text for term in OUT_OF_SCOPE_TERMS):
        return Classification(
            category="out_of_scope",
            risk_level="medium",
            rationale="La solicitud no corresponde a orientación social simulada.",
        )

    category = _category_from_text(text) or "general_orientation"
    if any(term in text for term in MEDIUM_RISK_TERMS):
        return Classification(
            category=category,
            risk_level="medium",
            rationale="Requiere guía, documentación o pasos concretos.",
        )

    return Classification(
        category=category,
        risk_level="low",
        rationale="Pregunta general de orientación.",
    )


def _category_from_text(text: str) -> str | None:
    for category, terms in CATEGORY_TERMS.items():
        if any(term in text for term in terms):
            return category
    return None
