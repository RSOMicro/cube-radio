<!--
---
name: Azure Functions Python HTTP Trigger using Azure Developer CLI
description: This repository contains an Azure Functions HTTP trigger quickstart written in Python and deployed to Azure Functions Flex Consumption using the Azure Developer CLI (azd). The sample uses managed identity and a virtual network to make sure deployment is secure by default. You can opt out of a VNet being used in the sample by setting VNET_ENABLED to false in the parameters.
page_type: sample
languages:
- azdeveloper
- python
- bicep
products:
- azure
- azure-functions
- entra-id
urlFragment: functions-quickstart-python-azd
---
-->

# Azure Functions Python HTTP Trigger using Azure Developer CLI

This template repository contains an HTTP trigger reference sample for Azure Functions written in Python and deployed to Azure using the Azure Developer CLI (`azd`). The sample uses managed identity and a virtual network to make sure deployment is secure by default.

This source code supports the article [Quickstart: Create and deploy functions to Azure Functions using the Azure Developer CLI](https://learn.microsoft.com/azure/azure-functions/create-first-function-azure-developer-cli?pivots=programming-language-python).

## Prerequisites

+ [Python 3.11](https://www.python.org/)
+ [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools)
+ [Azure Developer CLI (AZD)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
+ To use Visual Studio Code to run and debug locally:
  + [Visual Studio Code](https://code.visualstudio.com/)
  + [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)

## Run your app from the terminal

### Create a virtual environment

The way that you create your virtual environment depends on your operating system.
Open the terminal, navigate to the project folder, and run these commands:

### Linux/macOS/bash

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows (Cmd)

```shell
py -m venv .venv
.venv\scripts\activate
```

1. To start the Functions host locally, run these commands in the virtual environment:

    ```shell
    pip3 install -r requirements.txt
    func start
    ```

1. From your HTTP test tool in a new terminal (or from your browser), call the HTTP GET endpoint: <http://localhost:7071/api/httpget>

1. Test the HTTP POST trigger with a payload using your favorite secure HTTP test tool. This example uses the `curl` tool with payload data from the [`testdata.json`](./testdata.json) project file:

    ```shell
    curl -i http://localhost:7071/api/radio/remote -H "Content-Type: application/json"
    ```
	
You should get the list of radio stations

## Deploy to Azure
# Log in
az login

#Point to the right subscription
az account list --output table
az account set --subscription bc378d19-7df7-45c4-a370-a3b91453df99

# Create a storage account (required for Function App)
az storage account create --name mystorageacct123 --location westeurope --resource-group rso

# Create the Function App (Python 3.10)
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --name my-radio-function \
  --storage-account mystorageacct123
  
  Sadly this is not possible with Azure For student subscription...