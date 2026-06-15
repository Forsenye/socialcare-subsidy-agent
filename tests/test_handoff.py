from app.agent.classifier import classify_case
from app.agent.handoff import build_handoff_summary


def test_handoff_requires_human_for_high_risk_case() -> None:
    classification = classify_case("Hay amenaza contra un menor.")
    handoff = build_handoff_summary("Hay amenaza contra un menor.", classification)

    assert handoff["requires_human_advisor"] is True
    assert handoff["risk_level"] == "high"
