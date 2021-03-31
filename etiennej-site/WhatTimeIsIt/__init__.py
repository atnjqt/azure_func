import logging

import azure.functions as func

from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # THIS SIMPLE HTTP TRIGGER RETURNS THE TIME
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
             "This HTTP triggered function executed successfully.\n\n Current time of http trigger --> {}.".format(current_time),
             status_code=200
        )
