# Executive pitch

## Problem

People in vulnerable situations often need clear guidance about social subsidies, family support, and services for children, but their cases may be sensitive and require human care.

## Solution

SocialCare Subsidy Agent is a simulated AI assistant that offers clear Spanish guidance, retrieves controlled knowledge, applies Responsible AI rules, and escalates complex cases to a human advisor.

## Expected impact

- Faster first orientation for users.
- Lower risk of collecting unnecessary personal data.
- Better routing of sensitive cases.
- Reusable architecture for social-purpose digital services.

## Architecture

The prototype uses FastAPI, Streamlit, local Markdown RAG, safety rules, audit logging, and Azure-ready infrastructure. It is prepared for Azure AI Search and Microsoft Foundry Agent Service integration.

## Security

The project does not use real user data, confidential company data, or hardcoded secrets. Audit records mask sensitive values.

## Metrics

- Classification accuracy on simulated cases.
- Escalation rate for high-risk cases.
- Response groundedness against the knowledge base.
- Number of blocked sensitive-data requests.
- Demo response latency.

## Next steps

- Connect an Azure AI Search index.
- Configure Foundry Project Endpoint and model deployment.
- Add managed identity and RBAC.
- Expand evaluation datasets.
- Run supervised user testing with simulated scenarios.

## Positioning

This could be presented to an organization like Colsubsidio as an independent portfolio prototype inspired by social-purpose work, without stating that it is official or using private corporate information.
