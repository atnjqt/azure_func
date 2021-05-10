# Flask Python API Example

Etienne P Jacquot - 05/10/2021

This Python Flask app leverages the `ryp2` module to pass a pandas dataframe to the R module BCRA (more info [here](https://cran.r-project.org/web/packages/BCRA/index.html))

- For all configurations necessary for this workflow, please reference: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python

___________


## Build the app (LOCAL DEV)

Sample notebook here for testing --> [flask-app-testing.ipynb](./flask-app-testing.ipynb)


- steps to launch our testing Python Flask app (this is ok, really we want a serverless deployment option)

```
cd app
docker build --tag flask-bcra-app .
docker run --publish 5000:5000 -d flask-bcra-app

./deploy.sh
```

___________

## Azure Function Custom Linux Container for Python

More info here: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image

### Test local function

- Run the following for local test & dev (if no errors continue)

```bash
func start
```

- When ready to build, consider our `Dockerfile` which of course we customized for this example:

```diff
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

 # SET FOR SILENT R INSTALL
+ ENV DEBIAN_FRONTEND=noninteractive

# R DEPENDENCIES
+ RUN apt update && \
+     apt install -y r-base && \
+    R -e "install.packages('BCRA', repos='http://cran.rstudio.com/')"

# PYTHON DEPENDENCIES
+ RUN pip3 install azure-functions pandas rpy2

COPY . /home/site/wwwroot

```

We then build and run the docker container to ensure all is working

``` bash
docker build --tag atnjqt/azurefunctionspython:v1.0.3 . 
docker run -p 8080:80 -it atnjqt/azurefunctionspython:v1.0.3 

docker push atnjqt/azurefunctionspython:v1.0.3
```

## Deploy Azure Function 

We use the `azcli`, this uses existing ASC Azure resource group & storage groups that I have provisioned.

- Run the following:

```bash
az login

az functionapp plan create --resource-group asc-etienne-rg --name myPremiumPlan --location eastus2 --number-of-workers 1 --sku EP1 --is-linux

az functionapp create --name bcra-app-dev --storage-account etiennejapp --resource-group asc-etienne-rg --plan myPremiumPlan --runtime custom --deployment-container-image-name atnjqt/azurefunctionspython:v1.0.3

storageConnectionString=$(az storage account show-connection-string --resource-group asc-etienne-rg --name etiennejapp --query connectionString --output tsv)

az functionapp config appsettings set --name bcra-app-dev --resource-group asc-etienne-rg --settings AzureWebJobsStorage=$storageConnectionString
```

Great, you now created your Azure Function for `bcra-app-dev`!

- Navigate to the azure portal (https://portal.azure.com/) to get your api secret to access live function

- Sample URL (INCLUDE `code` FUNCTION SECRET) --> https://bcra-app-dev.azurewebsites.net/api/HttpExample?code=a8pePg8fmYYquKaU...ApGEq1mBNNA==&PID=0&T1=40&T2=45&N_Biop=1&HypPlas=99&AgeMen=14&Age1st=24&N_Rels=1&Race=1

___________

## Finally, use the Qualtrics API to pass values to our public endpoint

- More info here: https://www.qualtrics.com/support/integrations/api-integration/common-api-use-cases/

*I just setup a sample Qualtrics Survey **Web Servce** usecase and this works really nicely!!*


_________


## TODO...

- [ ] To have multiple functions for various bcra operations, this is probably an additional directory like [HttpExample](./HttpExample) ...
- [ ] qualtrics api use case to pass survey question values 
- [ ] set up branching for repo, or private bitbucket repository