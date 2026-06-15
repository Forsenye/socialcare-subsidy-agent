from __future__ import annotations

import streamlit as st

from app.agent.orchestrator import SocialCareAgent

st.set_page_config(page_title="SocialCare Subsidy Agent", page_icon="SC", layout="wide")

st.title("SocialCare Subsidy Agent")
st.caption(
    "Demo con datos simulados. No compartas documentos completos, contraseñas, cuentas bancarias "
    "ni información privada innecesaria."
)

agent = SocialCareAgent()

default_prompt = "Perdí mi empleo y quiero saber qué documentos generales podría revisar."
message = st.text_area("Consulta", value=default_prompt, height=120)

if st.button("Consultar", type="primary"):
    result = agent.answer(message)
    classification = result["classification"]
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

st.divider()
st.caption(
    "This project is inspired by my experience working in a social-purpose organization and uses "
    "simulated scenarios only, without exposing confidential company data or real user information."
)
