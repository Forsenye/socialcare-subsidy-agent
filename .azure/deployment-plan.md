# SocialCare Subsidy Agent Deployment Plan

Status: Ready for Validation

## Scope
- Create a local-first professional prototype for SocialCare Subsidy Agent.
- Prepare Azure-compatible infrastructure artifacts without deploying.
- Keep all data simulated and safe for portfolio, hackathon, and executive demo use.

## Architecture
- Python 3.11 FastAPI API service.
- Streamlit local demo UI.
- Local Markdown RAG with an adapter boundary for Azure AI Search and Microsoft Foundry Agent Service.
- Structured audit logging with masking.
- Azure Bicep scaffold for AI Search, Storage, Log Analytics, Application Insights, and Container Apps.
- GitHub Actions CI with Ruff, Pytest, and compile checks.

## Azure Services Planned
- Azure AI Search
- Azure Storage Account
- Log Analytics Workspace
- Application Insights
- Azure Container Apps Environment and App
- Environment variables for Azure OpenAI / Foundry model deployment

## Constraints
- No remote push.
- No Azure deployment.
- No secrets in source control.
- No real user data or corporate confidential data.
- No SDK-specific Foundry implementation unless the current API is confirmed.

## Validation
- python -m ruff check .
- python -m pytest
- python -m compileall app
- FastAPI import and route availability

## Handoff
- Manual Azure Foundry connection steps remain documented in docs/deployment_azure_foundry.md.
