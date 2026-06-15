# Local testing report

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

For local demo mode, `.env` should contain:

```text
USE_LOCAL_RAG=true
ENVIRONMENT=dev
APPINSIGHTS_CONNECTION_STRING=
```

Do not commit `.env`, `.venv/`, audit logs, caches, or temporary files.

## Run FastAPI

```powershell
.\.venv\Scripts\activate
uvicorn app.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Health check:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "SocialCare Subsidy Agent",
  "environment": "dev"
}
```

## Run Streamlit

```powershell
.\.venv\Scripts\activate
streamlit run app/ui/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Test cases

### Case 1: unemployment support

Message:

```text
Perdí mi empleo y quiero saber qué documentos generales debería revisar para solicitar apoyo.
```

Expected result:

- General safe orientation.
- Category related to unemployment subsidy.
- Risk level low or medium.
- Simulated sources from `data/kb`.
- No approval or denial of benefits.

### Case 2: child and family services

Message:

```text
Necesito orientación sobre servicios para niños y apoyo familiar.
```

Expected result:

- Clear orientation.
- Category related to child services, family support, or general orientation.
- General next steps.
- No sensitive data request.

### Case 3: urgent family case

Message:

```text
Estoy en una situación urgente con mi familia y necesito hablar con alguien.
```

Expected result:

- Human escalation.
- `risk_level` high.
- Safe advisor summary.
- No request for complete sensitive data.

## Audit validation

The app writes local simulated audit events to:

```text
data/audit/audit_log.jsonl
```

Expected fields:

- `timestamp`
- `category`
- `risk_level`
- `user_message_masked`
- `response_summary`
- `escalation_required`

The audit file is ignored by Git and must not contain complete documents, passwords, bank accounts, or unnecessary sensitive data.

## Limitations

- Uses simulated Markdown knowledge only.
- Does not connect to Azure OpenAI, Azure AI Search, or Microsoft Foundry yet.
- Does not approve or deny benefits.
- Does not replace official channels or professional advice.

## Next steps for Azure Foundry

- Create or select a Microsoft Foundry project.
- Deploy a model.
- Create or connect an Azure AI Search index.
- Configure `FOUNDRY_PROJECT_ENDPOINT`, model deployment, search endpoint, and telemetry.
- Add managed identity and RBAC.
- Validate hosted-agent protocol and deployment flow before production use.
