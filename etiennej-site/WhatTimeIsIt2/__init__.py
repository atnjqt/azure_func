import logging

import azure.functions as func
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    current_time = datetime.now().strftime("%H:%M:%S %D")

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
            "TEST & DEV FOR ASC IT -- Etienne & Naveen\n\n\n Current time of http trigger --> {}.\n\n Have a nice day!".format(current_time),
             status_code=200
        )
