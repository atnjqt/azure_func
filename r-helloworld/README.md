# Azure Functions - Custom Linux R Container for HTTP API Endpoint


- *Author:* [Etienne P Jacquot](mailto:epj@asc.upenn.edu) (04/29/2021)


## Getting Started

*Following the helpful Microsoft Azure Development example --> [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-other)*


- You need az cli, docker, and R on your localhost (I am running on MacOS):

``` bash
az login # <-- confirm you azure cli access

docker login # <-- confirm your Docker ID access

/Library/Frameworks/R.framework/Resources/bin/R --version # <-- to confirm local R version 
```
____________

## Develop your Local R Function 🌎 🌐 🚀

Local Azure Function R development to cloud Linux container


### Create our local Azure function project:

- *Azure Func Directory* --> [LocalFunctionsProject](./LocalFunctionsProject)

``` bash
func init LocalFunctionsProject --worker-runtime custom --docker
cd LocalFunctionsProject
func new --name HttpExample --template "HTTP trigger"
```

### Create your R HTTP handler script

- Run & add from the script which is described [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-other#create-and-test-the-local-functions-project). 

--> *YOU MUST GO TO THAT AZURE SITE TO COPY THE HANDLER R SCRIPT*

```bash
touch handler.R
vim handler.R
```
- Add the script for your R HTTPUV simple web app (more info [here](https://cran.r-project.org/web/packages/httpuv/index.html)) *

``` diff
+ library(httpuv)
+ ...
+ cat(paste0("Server listening on :", PORT, "...\n"))
+ runServer("0.0.0.0", PORT, app)
```

### Modify the hosts.json for custom R handler

Edit your [host.json](./LocalFunctionsProject/host.json) to add the following for a custom header

- We use the absolute path to my Rscript locally, *remember to change this for your local host / rebuild before pushing to Docker*

```diff
"customHandler": {
    "description": {
-      "defaultExecutablePath": "Rscript",
+      "defaultExecutablePath": "/Library/Frameworks/R.framework/Resources/bin/Rscript",
+      "arguments": [
+        "handler.R"
+      ]
```

### Test your R Azure Function locally (pre-container)

Test local R function on MacOS, I don't have this bin in my path so *local dev* edit the [host.json](./LocalFunctionsProject/host.json):

- Run the function locally to confirm this works as expected:

``` bash
/Library/Frameworks/R.framework/Resources/bin/R -e "install.packages('httpuv', repos='http://cran.rstudio.com/')"
func start
```

- This will show in browser http://localhost:7071/api/HttpExample

Significantly, to demonstrate how the Function api works you can append `&name=ETIENNEJ` to the url for a custom hello message. 

- This would be http://localhost:7071/api/HttpExample?name=ETIENNEJ


______________

## Turn your R Function into an Azure Linux Container 👨‍💻 ⛅ 🐳

With our R function working locally, proceed with containerizing

- Edit the [Dockerfile](./LocalFunctionsProject/Dockerfile)) with lines provided:s

```diff
+FROM mcr.microsoft.com/azure-functions/dotnet:3.0-appservice 
+ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
+    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

+RUN apt update && \
+    apt install -y r-base && \
+    R -e "install.packages('httpuv', repos='http://cran.rstudio.com/')"

+COPY . /home/site/wwwroot
```
- *PLEASE REMEMBER: Make sure to edit your [host.json](./LocalFunctionsProject/host.json) for the RScript line before building so this is not absolute path!!* 

### Build your container

Build your R function azure container locally:

- My dockerID is `atnjqt` --> https://hub.docker.com/u/atnjqt

``` bash
docker ps # <-- make sure Docker Daemon is on!

docker build --tag atnjqt/azurefunctionsimage:v1.0.0 .
```

### Run your container locally

Run your R function azure container locally:

- Make sure to use the correct version number 

``` bash
docker run -p 8080:80 -it atnjqt/azurefunctionsimage:v1.0.0
```

If you open http://localhost:8080 you will now notice the Azure Function default blue screen... 
- You can try and navigate to http://localhost:8080/api/HttpExample but this will fail! This is a security feature that can be limiting in dev for azure funcs... *You need to change `authlevel` to confirm this is working before pushing to the cloud!*

### *DEV STEP ONLY -->* Change auth level from function to anonymous

Edit your [HttpExample/function.json](./LocalFunctionsProject/HttpExample/function.json)

- You need to stop the local container, edit the following and restart docker daemon, then rebuild w/ a new tag version to run with anonymous authlevel:

```diff
  "bindings": [
    {
-     "authLevel": "function",
+     "authLevel": "anonymous",
      "type": "httpTrigger",
```

Please navigate to your API local endpoint, this should work locally now at http://localhost:8080/api/HttpExample
- Confirm the API function works w/ http://localhost:8080/api/HttpExample?name=ETIENNEJ-CONTAINER in `anonymous` authlevel enabled... 

*YOU MUST SWITCH BACK TO AUTHELEVEL `Function` FOR YOUR FUNCTION APP BEFORE DOCKER PUSH!* 

- i.e. Rebuild w/ a new tag, no need to rerun though because we know it works... 

_________

## Push your tested R Function Azure container image to Docker Hub

You can run the following, make sure to use the specific tag version number...

- initial push may take a while, but subsequent pushes are quick! 

``` bash
docker login

docker push atnjqt/azurefunctionsimage:v1.3.1
```

Navigate to docker hub to confirm your image is pushed to your account: 
- https://hub.docker.com/r/atnjqt/azurefunctionsimage/

___________

## Prepare your Azure Resources

Run the following examples to reproduce a public R http function endpoint.
- My organization already had various of these resources provisioned for my account / I was able to use already existing resources. I include the below steps just for reference, please consider associated costs w/ the premium EP1 linux instance...

### Create `Resource Group` & `Storage Group` (*OPTIONAL*)

- Run the following with specific values for `--name` values

``` bash
az login # <-- confirm your login to Azure

# Resource Group
az group create --name AzureFunctionsContainers-rg --location eastus2

az storage account create --name <storage_name> --location eastus2 --resource-group AzureFunctionsContainers-rg --sku Standard_LRS
```

### Create a `Premium App Plan` for Azure Functions (*REQUIRED*)

I already have the following so we just run: 
- resource groups (`asc-etienne-rg`) 
- storage groups (`etiennejapp`)

--> *NOTE, THIS IS A PREMIUM PLAN SO PLEASE DELETE WHEN COMPLETED!*

``` bash 
az functionapp plan create --resource-group asc-etienne-rg --name myPremiumPlan-dev --location eastus2 --number-of-workers 1 --sku EP1 --is-linux
```

Your premium App Service Plan is now created!
- *Please note we tried to find this on the GUI but couldn't find `EP1` ... *
______

## Create and configure a function app on Azure with the image

For our Aure Function we have the following configurations:

- `r-helloworld-dev` azure func name
- `etiennejapp` storage account name
- `asc-etienne-rg` resource group name
- `myPremiumPlan-dev` plan created in steps above
- `atnjqt/azurefunctionsimage:latest` as custom container (more info [here](https://hub.docker.com/r/atnjqt/azurefunctionsimage/tags?page=1&ordering=last_updated))

### Create your Azure Function App

We tried going through Azure GUI but unsure how to associate w/ a custom linux container

- Run the following for our `r-helloworld-dev`:

``` bash
az functionapp create --name r-helloworld-dev --storage-account etiennejapp --resource-group asc-etienne-rg --plan myPremiumPlan-dev --runtime custom --deployment-container-image-name atnjqt/azurefunctionsimage:v1.1.2
```

### Associate the Storage Account with our Azure Function App

- Run the following for storage account `etiennejapp` query string:

``` bash
storageConnectionString=$(az storage account show-connection-string --resource-group asc-etienne-rg --name etiennejapp --query connectionString --output tsv)

az functionapp config appsettings set --name r-helloworld-dev --resource-group asc-etienne-rg --settings AzureWebJobsStorage=$storageConnectionString
```

- Great! Your Azure Function is now associated with the Storage Account, and thus it should be live.

_____________

## Verify your Azure Function R-helloworld API

Navigate to https://portal.azure.com to find your Azure Function App
	
- https://r-helloworld-dev.azurewebsites.net (*to confirm the app is live*)

- https://r-helloworld-dev.azurewebsites.net/api/HttpExample (*our end point is public, but cannot be reached without Function level auth token*)
- https://r-helloworld-dev.azurewebsites.net/api/HttpExample?code=Vbl5n5NBSqFWObzJIbXgSKrro0RpeiEipEsIVaGgsADNvV84NtcI5w==  (*our end point is public and accessible w/ the function key included in HTTP query*)

### PASSING PARAMETERS TO OUR R HTTP API ENDPOINT

You can then pass query parameters, such as name, etc... 
- for an API call testing locally this works nicely, I think it's hard-coded in the example that it needs immediately after the URL `/api/HttpExample?name=YourNameHere&code=...`

- https://r-helloworld-dev.azurewebsites.net/api/HttpExample?name=Etienne_Azure_Testing...&code=Vbl5n5NBSqFWObzJIbXgSKrro0RpeiEipEsIVaGgsADNvV84NtcI5w==


### *TODO --> Using Azure Function w/ Qualtrics for Common API Use Case*

The idea I think is to pass a query string to the API that contains all the necessary BCRA columns... 
- More info on integration w/ Qualtrics API Common Use Cases here: https://www.qualtrics.com/support/integrations/api-integration/common-api-use-cases/


