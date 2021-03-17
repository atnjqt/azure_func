# Azure Functions Examples

Etienne P Jacquot - epj@asc.upenn.edu
(03/16/2021)

Simple examples for serverless computing using [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) to run python code!

Marlon brought to my attention a BestBuy URL to check if a local location has GPUs as sold out... Specifically, this url [here](https://www.bestbuy.com/site/canopy/component/fulfillment/fulfillment-summary/v1?context=compare&destinationZipCode=%24(csi.location.destinationZipCode)&deviceClass=l&locale=en-US&skuId=6439402&storeId=%24(csi.location.storeId)).
- Using Python modules `requests` & `beautifulsoup4` we can really easy check if it's sold out or not... *how can we automate this to check more frequently, and what can we do with the boolean TRUE/FALSE value that is returned?*

_______

## Getting Started 

This is all based on the great example from Microsoft here: [https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)

Please visit that page for system dependencies as there are quite a few! 

### Some steps I had to run on MacOS

- [Visual Studio Code](https://code.visualstudio.com/)
    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
    - [Azure Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos)
- [npm](https://www.npmjs.com/get-npm)
+ others ...

``` bash
# version 3.x for MacOS Python 3.8.x
npm install -g azure-functions-core-tools

# I had to update homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# to then install azure core tools for macos
brew tap azure/functions
brew install azure-functions-core-tools@3
# if upgrading on a machine that has 2.x installed
brew link --overwrite azure-functions-core-tools@3
```
________

## Test Project as Azure Function



### Deploying from local Macbook to Azure Fuction using VS Code:

In Visual Studio Code you can open a new project, set it to [test-project](./test-project/) with my default `/usr/bin/python3` and it creates it's own virtual envirment...

--> Python code [HttpTrigger-testing/__init__.py](./test-project/HttpTrigger-testing/__init__.py)
- this contains a simple function which checks if the url is SOLD OUT or not
- Again this is just a quick example for using python code... This is based on the HTTP Trigger template

--> requirements [requirements.txt](./test-project/requirements.txt)
- add any python pip installs to your req file if needed

``` diff
azure-functions
+beautifulsoup4
+requests%    
```

Once you run and deploy on your http://localhost:7071 and this is working as expected go ahead and deploy your endpoint to Azure Functions... You can then check the public facing endpoint. 

## TODO

-->> Better python code example than http trigger template
-->> Getting Started section should be more detailed for MacOS developers...
-->> docker container deployment of azure functions (does not support consumption model only premium)