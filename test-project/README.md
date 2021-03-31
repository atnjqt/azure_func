# Test Project for Azure Function

**UPDATE (03/30/2021)**: This was the first example I did for Azure Function testing, looking at the best buy ULR as referenced. Turns out Marlon found a chrome plungin extension which monitors a site for delta changes to a specific section of HTML. We also explored [Azure Automation Runbooks](https://docs.microsoft.com/en-us/azure/automation/automation-quickstart-create-runbook) as another serverless computing service which is maybe better than functions (automation vs public endpoint).

## Getting Started

Marlon brought to my attention a BestBuy URL to check if a local location has GPUs as sold out... Specifically, this url [here](https://www.bestbuy.com/site/canopy/component/fulfillment/fulfillment-summary/v1?context=compare&destinationZipCode=%24(csi.location.destinationZipCode)&deviceClass=l&locale=en-US&skuId=6439402&storeId=%24(csi.location.storeId)).

- Using Python modules `requests` & `beautifulsoup4` we can really easy check if it's sold out or not... (example, this checks on another URL and uses BeautifulSoup to extract that HTML into an HTTPResponse)

## Deploying from local Macbook to Azure Fuction using VS Code:

In Visual Studio Code, open a new project and set it to [test-project](./test-project/) with my default `/usr/bin/python3`, this will create a virtual envirment for the project.

### *Your Azure Function Python HTTPTrigger Files:*

--> Python code [HttpTrigger-testing/__init__.py](./test-project/HttpTrigger-testing/__init__.py)
- this contains a simple function which checks if the url is SOLD OUT or not. Always will be the **__init__.py** for these type of examples.

--> requirements [requirements.txt](./test-project/requirements.txt)
- add any python pip installs to your req file if needed

``` diff
azure-functions
+beautifulsoup4
+requests%    
```

Run you test & dev by deploying on your local machine with `f5` --> [http://localhost:7071/api/httptrigger-testing](http://localhost:7071/api/httptrigger-testing) to confirm this is working as expected and upload to Azure.

_______

## Deploying on Azure Portal to Live Environment

On your Azure portal dashboard, start your Azure Function project.

- The site is accessible at [https://bestbuy-soldout-checker.azurewebsites.net/api/httptrigger-testing](https://bestbuy-soldout-checker.azurewebsites.net/api/httptrigger-testing)

*Do not forget to power down when not in use, to avoid charges...*
