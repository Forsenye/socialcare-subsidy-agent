# Architecture

SocialCare Subsidy Agent is a local-first enterprise prototype for safe social subsidy orientation. It separates user channels, policy orchestration, retrieval, safety checks, human handoff, and audit logging.

## Components

- Streamlit UI for a fast executive demo.
- FastAPI service with `/health`, `/chat`, `/classify`, and `/handoff`.
- Classifier for case category and risk level.
- Local Markdown RAG for simulated knowledge.
- Safety module for sensitive-data handling and response limits.
- Handoff module for safe advisor summaries.
- Audit log in JSONL with masked user messages.
- Bicep infrastructure scaffold for Azure deployment readiness.

## Azure target

The production path can map the API container to Azure Container Apps, telemetry to Application Insights, search to Azure AI Search, and orchestration to Microsoft Foundry Agent Service. The current implementation keeps a clean adapter boundary to avoid hardcoding preview SDK behavior.
