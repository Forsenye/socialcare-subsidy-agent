from app.agent.classifier import classify_case


def test_classifies_unemployment_subsidy_as_medium_when_documents_are_requested() -> None:
    result = classify_case("Perdí mi empleo y necesito saber documentos para el subsidio.")

    assert result.category == "unemployment_subsidy"
    assert result.risk_level == "medium"


def test_classifies_job_loss_without_subsidy_keyword() -> None:
    result = classify_case("Perdí mi empleo y quiero saber qué documentos generales debo revisar.")

    assert result.category == "unemployment_subsidy"
    assert result.risk_level == "medium"


def test_classifies_child_risk_as_high() -> None:
    result = classify_case("Hay posible maltrato a un menor y necesito ayuda urgente.")

    assert result.category == "child_services"
    assert result.risk_level == "high"
