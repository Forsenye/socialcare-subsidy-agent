# Azure and Microsoft Foundry deployment guide

This repository intentionally avoids a hard dependency on a specific Foundry SDK surface because hosted-agent APIs are evolving. The code keeps an adapter boundary in `app/agent/orchestrator.py`.

## Manual steps

1. Create or select a Microsoft Foundry project.
2. Deploy a model from the Foundry model catalog.
3. Create an Azure AI Search service and index for the simulated knowledge base.
4. Configure environment variables:
   - `FOUNDRY_PROJECT_ENDPOINT`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_DEPLOYMENT`
   - `AZURE_OPENAI_API_VERSION`
   - `AZURE_AI_SEARCH_ENDPOINT`
   - `AZURE_AI_SEARCH_INDEX`
   - `APPINSIGHTS_CONNECTION_STRING`
5. Package the API as a container.
6. Deploy to Azure Container Apps or Foundry hosted agents after confirming the current hosted-agent protocol.
7. Assign managed identity permissions to Azure AI Search and telemetry resources.
8. Register agent instructions from `app/agent/instructions.md`.
9. Connect search as a tool or knowledge source.
10. Run evaluation with `data/samples/evaluation_dataset.json`.

## Deployment commands

Prepare locally:

```bash
docker build -t socialcare-subsidy-agent .
docker compose up --build
```

Azure Developer CLI path after environment selection:

```bash
azd auth login
azd env new dev
azd provision
azd deploy
```

Do not run deployment commands until subscription, region, quotas, identity, network, and secret-management decisions are approved.

## Official references checked

- Microsoft Learn: Hosted agents in Foundry Agent Service (preview)
  <https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents>
- Microsoft Learn: What is Microsoft Foundry Agent Service?
  <https://learn.microsoft.com/en-us/azure/foundry/agents/overview>
- Microsoft Learn: Quickstart to deploy a hosted agent
  <https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-hosted-agent>
- Microsoft Learn: Azure Developer CLI AI agent extension
  <https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/extensions/azure-ai-foundry-extension>
