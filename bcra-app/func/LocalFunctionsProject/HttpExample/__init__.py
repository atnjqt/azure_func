# Etienne P Jacquot - 05/1-/2021

import logging

import azure.functions as func

import pandas as pd

# Allow R Package import
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages

# Allow conversion for dataframes
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

# BCRA Python to R Function
def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Prepare logging
    logging.info('Python HTTP trigger function processed a BCRA check summary request.')

    # Prepare DataFrame from HTTP request
    PID = int(req.params.get('PID'))
    T1 = int(req.params.get('T1'))
    T2 = int(req.params.get('T2'))
    N_Biop = int(req.params.get('N_Biop'))
    HypPlas = int(req.params.get('HypPlas'))
    AgeMen = int(req.params.get('AgeMen'))
    Age1st = int(req.params.get('Age1st'))
    N_Rels = int(req.params.get('N_Rels'))
    Race = int(req.params.get('Race'))
    T1 = int(req.params.get('T1'))

    logging.info('http values passed...')

    # Create dataframe from HTTP get values:
    df = pd.DataFrame({'id':PID,
              'T1':T1,
              'T2':T2,
              'N_Biop':N_Biop,
              'HypPlas':HypPlas,
              'AgeMen':AgeMen,
              'Age1st':Age1st,
              'N_Rels':N_Rels,
              'Race':Race},index=['id'])

    logging.info('df created..')

    ##########################################    
    # Load R Package for BCRA
    bcra = importr('BCRA')

    logging.info('BCRA R package loaded ...')

    # Add BCRA Functions here
    check_summary = bcra.check_summary
    absolute_risk = bcra.absolute_risk

    # Convert to R dataframe
    pandas2ri.activate()
    r_dt = ro.conversion.py2rpy(df) # df is a pd.DataFrame object

    # return check summary bcra result
    return func.HttpResponse(
            'absolute_risk (DEVELOPEMENT) --> {}\n\ncheck summary:\n{}\n\nepj@asc.upenn.edu'.format(absolute_risk(r_dt),check_summary(r_dt).to_dict()),
            status_code=200)
    
    #if not name:
    #    try:
    #        req_body = req.get_json()
    #    except ValueError:
    #        pass
    #    else:
    #        name = req_body.get('name')
    #if name:
    #    return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    #else:
    #    return func.HttpResponse(
    #        "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #         status_code=200)