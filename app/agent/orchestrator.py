from __future__ import annotations

from dataclasses import asdict

from app.agent.classifier import Classification, classify_case
from app.agent.handoff import build_handoff_summary
from app.agent.rag import LocalMarkdownRag, SearchResult
from app.agent.safety import (
    contains_sensitive_data_request,
    enforce_response_boundaries,
    requires_safety_escalation,
)


class SocialCareAgent:
    def __init__(self, rag: LocalMarkdownRag | None = None) -> None:
        self.rag = rag or LocalMarkdownRag()

    def answer(self, user_message: str) -> dict[str, object]:
        classification = classify_case(user_message)
        retrieved = self.rag.search(user_message)
        escalation_required = requires_safety_escalation(user_message, classification.risk_level)
        response = self._compose_response(
            user_message,
            classification,
            retrieved,
            escalation_required,
        )
        handoff = build_handoff_summary(user_message, classification)
        return {
            "classification": asdict(classification),
            "response": response,
            "sources": [result.__dict__ for result in retrieved],
            "escalation_required": escalation_required,
            "handoff": handoff,
        }

    def _compose_response(
        self,
        user_message: str,
        classification: Classification,
        retrieved: list[SearchResult],
        escalation_required: bool,
    ) -> str:
        if contains_sensitive_data_request(user_message):
            return enforce_response_boundaries(
                "Por seguridad, no compartas contraseñas, cuentas bancarias, documentos completos "
                "ni códigos. Puedo orientarte con información general y, si el caso lo requiere, "
                "preparar un resumen seguro para un asesor humano."
            )

        if classification.category == "out_of_scope":
            return enforce_response_boundaries(
                "Este prototipo solo orienta sobre subsidios sociales simulados, apoyo familiar, "
                "servicios para niños y canales de atención. Para otros temas, usa una fuente "
                "oficial o un asesor especializado."
            )

        context = "\n".join(f"- {result.snippet}" for result in retrieved) or (
            "- No encontré una coincidencia suficiente en la base simulada."
        )
        next_step = (
            "Por la sensibilidad del caso, recomiendo hablar con un asesor humano y usar "
            "canales oficiales."
            if escalation_required
            else "Como siguiente paso, revisa los requisitos generales y valida la información "
            "en un canal oficial."
        )
        response = (
            "Te puedo orientar de forma general y segura con base en información simulada.\n\n"
            f"Clasificación: {classification.category} ({classification.risk_level}).\n\n"
            "Información relevante encontrada:\n"
            f"{context}\n\n"
            f"{next_step}\n\n"
            "Evita compartir datos sensibles completos en este canal."
        )
        return enforce_response_boundaries(response)


# Future Foundry Agent Service integration:
# - Use FOUNDRY_PROJECT_ENDPOINT and model deployment from environment variables.
# - Keep this orchestrator as the local business-policy boundary.
# - Register RAG/search as a tool or connect an Azure AI Search knowledge index.
# - Use managed identity for hosted agent and downstream Azure resources.
