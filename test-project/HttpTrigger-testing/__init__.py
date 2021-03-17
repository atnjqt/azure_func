import logging
import azure.functions as func
## ETIENNE CODE BELOW FOR TESTING...
from bs4 import BeautifulSoup
import requests

############################
## USING A FUNCTION TO PASS URL & HEADERS
def check_if_sold_out(bestbuy_url,custom_headers):
    result = 'Sold Out' in str(BeautifulSoup(requests.get(bestbuy_url, headers=custom_headers).text,'html.parser').find(class_='fulfillment-fulfillment-summary').find('strong'))
    if result == True:
        return 'val is {}, item is SOLD OUT'.format(result)
    else:
        return 'val is {}, this should be available'.format(result)

############################
## DEFAULT HTTP TRIGGER INCLUDING MY FUNCTION:

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ############################   
    ## SET YOUR URL OF INTEREST FROM BESTBUY    
    url = 'https://www.bestbuy.com/site/canopy/component/fulfillment/fulfillment-summary/v1?context=compare&destinationZipCode=%24(csi.location.destinationZipCode)&deviceClass=l&locale=en-US&skuId=6439402&storeId=%24(csi.location.storeId)'
    ## SET YOUR HEADERS (DEFAULT USER AGENT IS BLACKLISTED)
    headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'USER@asc.upenn.edu'  # This is another valid field
    }

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:

        return func.HttpResponse(
             "This Sample Azure HTTP triggered function executed successfully.\n\nPass a name in the query string or in the request body for a personalized response.\n\nURL:\n{}\n\n---> {}".format(url,check_if_sold_out(url,headers)),
             status_code=200
        )