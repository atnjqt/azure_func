# Azure Functions Examples

Etienne P Jacquot - epj@asc.upenn.edu
(03/30/2021)

Simple examples for serverless computing using [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) to run python code!

## Getting Started 🦾 

This repository is based on the example from Microsoft here: [https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python). 

### *System Dependencies for Azure Function dev 💻*:

Please visit for Microsoft's detailed instructions on system dependencies. These include the following:

<img width='250' src='https://1.bp.blogspot.com/-ZJIo7wY3m9o/XsWe4ZqT3GI/AAAAAAAAGjU/JW25MQzC2-YPwXWuiD0-Nfn3BGYphTISwCLcBGAsYHQ/s1600/AzureFunctionsPython.png'/> 

- [Visual Studio Code](https://code.visualstudio.com/) with the following add-on features:
    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
    - [Azure Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos)
- NodeJS & [npm](https://www.npmjs.com/get-npm)

Had to also run the following in MacOS terminal:

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

## My Dev Projects & Functions:

Each Azure Function project should have a directory in this repository, and each respective project can have many different functions. For simplicity so far each project only has one function.

- My first azure function example for best buy url: [test-project](./test-project)

- Simple example created using Visual Studio Code: [etiennej-site](./etiennej-site)
    - I'll likely get rid of the original best buy and continue dev work inside of etiennej-site#


### Examples for using Azure Functions in Data Science Projects... ? 

Use `curl` to get your site when live! 

- Example here: [httpTrigger_result.ipynb](./httpTrigger_result.ipynb)

__________

## TODO

-->> figure out odd time +4 hour dif for us-east-2 on whattimeisit functions

-->> docker container deployment of azure functions (does not support consumption model only premium)

![](https://www.koskila.net/wp-content/uploads/2019/05/tenor.gif)
