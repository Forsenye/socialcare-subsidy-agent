from __future__ import annotations

import streamlit as st

from app.agent.orchestrator import SocialCareAgent
from app.core.audit import write_audit_event

st.set_page_config(page_title="SocialCare Subsidy Agent", page_icon="SC", layout="wide")

SAMPLE_CASES = {
    "Subsidio por desempleo": (
        "Perdí mi empleo y quiero saber qué documentos generales debería revisar "
        "para solicitar apoyo."
    ),
    "Niñez y familia": "Necesito orientación sobre servicios para niños y apoyo familiar.",
    "Caso urgente": "Estoy en una situación urgente con mi familia y necesito hablar con alguien.",
}

st.title("SocialCare Subsidy Agent")
st.caption(
    "Demo con datos simulados. No compartas documentos completos, contraseñas, cuentas bancarias "
    "ni información privada innecesaria."
)

agent = SocialCareAgent()

if "message" not in st.session_state:
    st.session_state.message = SAMPLE_CASES["Subsidio por desempleo"]

with st.sidebar:
    st.header("Casos demo")
    for label, prompt in SAMPLE_CASES.items():
        if st.button(label, use_container_width=True):
            st.session_state.message = prompt
    st.divider()
    st.caption(
        "El prototipo usa una base de conocimiento Markdown local y no requiere claves de Azure."
    )

message = st.text_area("Consulta", key="message", height=130)

if st.button("Consultar", type="primary"):
    result = agent.answer(message)
    classification = result["classification"]
    write_audit_event(
        category=str(classification["category"]),
        risk_level=str(classification["risk_level"]),
        user_message=message,
        response_summary=str(result["response"]),
        escalation_required=bool(result["escalation_required"]),
    )

    st.success("Consulta procesada con RAG local simulado.")
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Respuesta")
        st.write(result["response"])
        st.subheader("Fuentes simuladas")
        for source in result["sources"]:
            st.markdown(f"- **{source['title']}** `{source['source']}`")
    with right:
        st.subheader("Clasificación")
        st.json(classification)
        st.subheader("Escalamiento")
        st.metric("Requiere asesor humano", "Sí" if result["escalation_required"] else "No")
        st.subheader("Resumen seguro")
        st.json(result["handoff"])
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Modo", "Local RAG")
    col2.metric("Datos", "Simulados")
    col3.metric("Azure", "Sin claves")

st.divider()
st.caption(
    "This project is inspired by my experience working in a social-purpose organization and uses "
    "simulated scenarios only, without exposing confidential company data or real user information."
)
