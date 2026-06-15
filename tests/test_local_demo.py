from app.agent.orchestrator import SocialCareAgent


def test_demo_unemployment_case_uses_local_rag() -> None:
    agent = SocialCareAgent()
    result = agent.answer(
        "Perdí mi empleo y quiero saber qué documentos generales debería revisar "
        "para solicitar apoyo."
    )

    assert result["classification"]["category"] == "unemployment_subsidy"
    assert result["classification"]["risk_level"] in {"low", "medium"}
    assert result["sources"]
    assert "no aprueba ni niega" in result["response"].lower()


def test_demo_child_family_case_is_relevant() -> None:
    agent = SocialCareAgent()
    result = agent.answer("Necesito orientación sobre servicios para niños y apoyo familiar.")

    assert result["classification"]["category"] in {
        "child_services",
        "family_support",
        "general_orientation",
    }
    assert result["sources"]


def test_demo_urgent_family_case_requires_handoff() -> None:
    agent = SocialCareAgent()
    result = agent.answer(
        "Estoy en una situación urgente con mi familia y necesito hablar con alguien."
    )

    assert result["classification"]["risk_level"] == "high"
    assert result["escalation_required"] is True
    assert result["handoff"]["requires_human_advisor"] is True
