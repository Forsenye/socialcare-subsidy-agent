from app.agent.safety import (
    contains_sensitive_data_request,
    mask_sensitive_data,
    response_has_unsafe_decision,
)


def test_detects_sensitive_data_request() -> None:
    assert contains_sensitive_data_request("Te puedo enviar mi contraseña y cuenta bancaria?")


def test_masks_sensitive_values() -> None:
    masked = mask_sensitive_data("Mi documento es 1234567890 y mi clave es secreta")

    assert "1234567890" not in masked
    assert "[DATO_ENMASCARADO]" in masked


def test_detects_unsafe_decision_language() -> None:
    assert response_has_unsafe_decision("Tu subsidio fue aprobado.")
