# Etienne P Jacquot - 05/11/2021

# LOCAL TEST & DEV ONLY, OS environment path for R
#import os
#os.environ['R_HOME'] = '/Library/Frameworks/R.framework/Resources/'

import logging

import azure.functions as func

import pandas as pd
import json

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
        logging.info('Python HTTP trigger function processed a BCRA absolute_risk request.')

        # Prepare DataFrame from HTTP GET request
        try:
                PID = int(req.params.get('PID'))
        except:
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"PID failed for participant index...",
                                "ERROR_VAL":req.params.get('PID')}),
                                status_code=400)

        try:
                T1 = int(req.params.get('T1'))
        except:
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"T1 failed for participant age...",
                                "ERROR_VAL":req.params.get('T1')}),
                                status_code=400)
        try:
                T2 = int(req.params.get('T2'))
        except:
                #T2 = T1 + 10 # <-- 10 year risk calculation, manually defined
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"T2 failed for projected age...",
                                "ERROR_VAL":req.params.get('T2')}),
                                status_code=400)

        try:
                N_Biop = int(req.params.get('N_Biop'))
        except:
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"N_Biop failed for biops...",
                                "ERROR_VAL":req.params.get('N_Biop')}),
                                status_code=400)

        try:
                HypPlas = int(req.params.get('HypPlas'))
        except:
                HypPlas = int('99') # <-- this we can just set as unknown if no val
                #return func.HttpResponse(
                #        json.dumps({"ERROR_MSG":"HypPlas failed for hyperplasia -- 99 unknown?...",
                #               "ERROR_VAL":req.params.get('HypPlas')}),
                #               status_code=400)

        try:
                AgeMen = int(req.params.get('AgeMen'))
        except:
                # maybe we need a dict which matches the qualtrics categorical responses to num?
                # or flags in BCRA for this? not sure ... 
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"AgeMen failed... is this categorical or numeric?",
                                "ERROR_VAL":req.params.get('AgeMen')}),
                                status_code=400)
        try:
                Age1st = int(req.params.get('Age1st'))
        except:
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"Age1st failed... is this categorical or numeric?",
                                "ERROR_VAL":req.params.get('Age1st')}),
                                status_code=400)
        try:                
                N_Rels = int(req.params.get('N_Rels'))
        except:
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"N_Rels failed for number of relatives w/ BCRA...",
                                "ERROR_VAL":req.params.get('Age1st')}),
                                status_code=400)
        try:        
                Race = int(req.params.get('Race'))
        except:
                # maybe we need a dict which matches the qualtrics categorical response to numeric val for race
                return func.HttpResponse(
                        json.dumps({"ERROR_MSG":"Race failed for val...",
                                "ERROR_VAL":req.params.get('Race')}),
                                status_code=400)


        logging.info('HTTP get request syntax ok...')

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

        logging.info('Response df created ...')

        ##########################################    
        # Load R Package for BCRA

        bcra = importr('BCRA')

        logging.info('BCRA R package loaded ...')

        # Add BCRA Functions here
        #check_summary = bcra.check_summary
        absolute_risk = bcra.absolute_risk
        #error_check = bcra.error_check
        relative_risk = bcra.relative_risk

        # Convert to R dataframe
        pandas2ri.activate()
        r_dt = ro.conversion.py2rpy(df) # df is a pd.DataFrame object

        logging.info('Calculating absolute risk (DEV) ...')

        # Return check summary bcra result
        # Qualtrics embedded data is json structure
        return func.HttpResponse(
                json.dumps({"absolute_risk":absolute_risk(r_dt).tolist()[0],
                            "relative_risk":relative_risk(r_dt).to_dict()}),
                status_code=200)