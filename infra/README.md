# Azure infrastructure

This folder contains a Bicep scaffold for a local-first prototype.

Resources:
- Azure AI Search for future RAG indexing.
- Storage Account for supporting artifacts.
- Log Analytics and Application Insights for observability.
- Azure Container Apps for hosting the FastAPI container.
- Managed identity placeholder for secretless access.

No deployment is executed by this repository. Use `azd provision` or `az deployment group create` only after selecting a subscription, resource group, region, model deployment, and Foundry project endpoint.
