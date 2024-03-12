# bubi-azure-uploader

This is an Azure function that runs every 10 minutes, downloads the BUBI status JSON from the web and saves it into an Azure storage account.

## How to deploy
Run `func azure functionapp publish bubiscraper --build remote` in the VSCode terminal.

## How to set up access keys for the storage account
When the function is created, a storage account is created with it, as well. In VSCode command palette, run `Azure Functions: Download remote settings`. This will overwrite the local.settings.json, which contains the connection string in the field `AzureWebJobsStorage`. This file must remain local and should not be checked into Git.

## How to configure the blob output
In the `@app.blob_output` decorator, we must specify the name of the connection string parameter, `AzureWebJobsStorage`. We must also add the output filename together with the container name, such as `path="bubi-jsons/{DateTime}.json"`. With this, the output will be saved into the `bubi-jsons` container, and the name will be the current UTC time.
