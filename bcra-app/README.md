# Python + R API Example (Azure Function)

Etienne P Jacquot - 05/11/2021

## *DEVELOPMENT WORK FOR DECIDE2SCREEN-DEV!*

Please visit [func](./func) for latest example 
- live example (no key though)--> https://bcra-app.azurewebsites.net/api/HttpExample?code=e8vidzhvAgnIt...I7SJpyqQ==&PID=0&T1=40&T2=45&N_Biop=1&HypPlas=99&AgeMen=14&Age1st=24&N_Rels=1&Race=3
- qualtric public example --> https://upenn.co1.qualtrics.com/jfe/form/SV_1TgqHuxZFvSlf4W

This Azure Function Python HTTP Trigger leverages the `ryp2` module to pass a pandas dataframe (created by GET request) to an R module (specifically, `BCRA`, more info [here](https://cran.r-project.org/web/packages/BCRA/index.html))

- For all configurations required for this workflow, please reference Microsoft's helpful guide for getting started: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python

- The goal of this project is to deploy an azure function to then supercharge a Qualtrics survey following the *common api use case* described [here](https://www.qualtrics.com/support/integrations/api-integration/common-api-use-cases/). Significantly, we pass results to our python function which then computes the BCRA **absolute_risk** score which is returned in the survey to participants.

___________

## Azure Function Custom Linux Container for Python

More info here: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image

### Getting Started w/ Azure Function

Create a new directory on your host. Microsoft recommends setting up a virtual environment for this directory so you can do your respective pip installs for local azure function testing...

- Configure your venv

```bash
# setup a folder for your new app (name it whatever youw want!) 
mkdir bcra_func_testing
cd bcra_func_testing

# setup your python virtual env for this specific project...
python3 -m venv .venv
source .venv/bin/activate
```

- Start a new Python Custom Linux project

```bash
func init LocalFunctionsProject --worker-runtime python --docker
cd LocalFunctionsProject
```

- Create a new function based on the HTTP trigger template

```bash
func new --name HttpExample --template "HTTP trigger"
func start
```

### Develop your local function

Make your changes to [func/LocalFunctionsProject/-_init_-.py](./func/LocalFunctionsProject/), this is the Python script that gets fired off when the function is reached via URL.

- Run the following to test & confirm your local test & dev

```bash
func start
```

- When your function is working locally, you are ready to build! 

Consider our `Dockerfile` which of course we customized for this example:


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

Proceed with building, running, and pushing the docker container to ensure all is working 
- *remember to set your tag version number!*
- Note: my login is `atnjqt`, you need your own [Docker login](https://hub.docker.com/account/login/)

``` bash
docker build --tag atnjqt/azurefunctionspython:v1.1.0 . 

# OPTIONAL step to confirm http://localhost:8080/
# See the microsoft guide on AuthLevel Anonymous (dev) vs Function (prod)
docker run -p 8080:80 -it atnjqt/azurefunctionspython:v1.1.0 

docker push atnjqt/azurefunctionspython:v1.1.0
```

## Deploy Azure Function 

We use the `azcli`, this uses existing ASC Azure resource group & storage groups that I have provisioned.

- Run the following:

```bash
az login

az functionapp plan create --resource-group asc-etienne-rg --name myPremiumPlan --location eastus2 --number-of-workers 1 --sku EP1 --is-linux

az functionapp create --name bcra-app --storage-account etiennejapp --resource-group asc-etienne-rg --plan myPremiumPlan --runtime custom --deployment-container-image-name atnjqt/azurefunctionspython:v1.1.0

storageConnectionString=$(az storage account show-connection-string --resource-group asc-etienne-rg --name etiennejapp --query connectionString --output tsv)

az functionapp config appsettings set --name bcra-app --resource-group asc-etienne-rg --settings AzureWebJobsStorage=$storageConnectionString
```

Great, you now created your Azure Function for `bcra-app`!

- Navigate to the azure portal (https://portal.azure.com/) to get your api secret to access the public function endpoint

Sample URL (INCLUDE `code` FUNCTION SECRET) --> 
- https://bcra-app-dev.azurewebsites.net/api/HttpExample?code=a8pePg8fmYYquKaU...ApGEq1mBNNA==&PID=0&T1=40&T2=45&N_Biop=1&HypPlas=99&AgeMen=14&Age1st=24&N_Rels=1&Race=1

### Enable CICD for your Azure Function Docker image

- Run the following for your azure function app

```bash
az functionapp deployment container config --enable-cd --query CI_CD_URL --output tsv --name bcra-app --resource-group asc-etienne-rg
```

- Copy the web hook url (sample, https://$bcra-app:L1YfjGLbz...4lsAq3SENFMi@bcra-app.scm.azurewebsites.net/docker/hook) and load it as a repository webhook for the respective image! 

- On subsequent docker image pushes, your azure function should automatically pull the latest image! I noticed ~1 minute delay from push to when the public endpoint was continously deployed!

___________

## Finally, use the Qualtrics API to pass values to our public endpoint

- More info here: https://www.qualtrics.com/support/integrations/api-integration/common-api-use-cases/

*I just setup a sample Qualtrics Survey **Web Servce** usecase and this works really nicely!!*

- Please visit https://upenn.co1.qualtrics.com/jfe/form/SV_1TgqHuxZFvSlf4W for a public demonstration of the BCRA absolute risk calculator. (all values are numeric!)

_________


## TODO --> ...

Okay so the AZ Func is really a nice way to BYOA (Bring-Your-Own-API)... This represents great progress but still a lot to go!

- [ ] To have *multiple functions* for various bcra operations, this is probably an additional directory like [HttpExample](./HttpExample) ...

- [X] Review *Qualtrics api* use case to pass survey question values, piped values ... This is *embedded data* I believe.

- [ ] set up *branching* for repo, or private bitbucket repository

- [ ] enable *CICD* for this development project so qualtrics survey always gets latest api endpoint results

- [ ] look at *azure resource consumption* for estimates over lifecycle of decide2screen project 

- [ ] demo presentation for this work w/ emphasis on serverless computing + qualtrics survey -- *dev for best of both worlds*