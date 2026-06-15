targetScope = 'resourceGroup'

@description('Base name used for Azure resources.')
param name string = 'socialcare-agent'

@description('Azure region for resources.')
param location string = resourceGroup().location

@description('Container image to deploy after CI/CD publishes it.')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

@description('Azure OpenAI or Foundry model deployment name. Do not put secrets here.')
param azureOpenAiDeployment string = ''

@description('Microsoft Foundry Project Endpoint. Do not put secrets here.')
param foundryProjectEndpoint string = ''

var normalized = toLower(replace(name, '-', ''))
var storageName = take('${normalized}st${uniqueString(resourceGroup().id)}', 24)

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${name}-law'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${name}-appi'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource search 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: '${name}-search'
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
    disableLocalAuth: false
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    replicaCount: 1
    partitionCount: 1
  }
}

resource environment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${name}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${name}-id'
  location: location
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${name}-api'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
    }
    template: {
      containers: [
        {
          name: 'api'
          image: containerImage
          env: [
            {
              name: 'ENVIRONMENT'
              value: 'dev'
            }
            {
              name: 'USE_LOCAL_RAG'
              value: 'false'
            }
            {
              name: 'AZURE_AI_SEARCH_ENDPOINT'
              value: 'https://${search.name}.search.windows.net'
            }
            {
              name: 'AZURE_AI_SEARCH_INDEX'
              value: 'socialcare-kb'
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: azureOpenAiDeployment
            }
            {
              name: 'FOUNDRY_PROJECT_ENDPOINT'
              value: foundryProjectEndpoint
            }
            {
              name: 'APPINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
      }
    }
  }
}

output applicationInsightsConnectionString string = appInsights.properties.ConnectionString
output searchEndpoint string = 'https://${search.name}.search.windows.net'
output containerAppUrl string = 'https://${app.properties.configuration.ingress.fqdn}'

// Microsoft Foundry Agent Service connection notes:
// - Use managed identity for hosted agent and downstream Azure resources.
// - Connect the Foundry project endpoint and model deployment via environment variables.
// - Create or connect an Azure AI Search index named by AZURE_AI_SEARCH_INDEX.
// - Avoid hardcoded keys; prefer RBAC or Key Vault for production.
