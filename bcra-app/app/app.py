# Etienne P Jacquot - 05/09/2021

import flask
from flask import request, jsonify
import pandas as pd

# Allow R Package import
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages

# Allow conversion for dataframes
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

app = flask.Flask(__name__)
app.config["DEBUG"] = True

from flask import Flask
app = Flask(__name__)


# Default landing hello world page 
@app.route('/')
def hello_world():
    return '<h1>Hello World, ATN!<h1><p>Testing API on http://0.0.0.0:5000/api/example_df for df to R script ...'


@app.route('/api/check_summary', methods=['GET'])
def api_id():
    # Check if values are provided in HTTP request
    # This takes values as numbers which is required for BCRA
    
    if 'id' in request.args:
        PID = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    
    if 'T1' in request.args:
        T1 = int(request.args['T1'])
    else:
        return "Error: No T1 field provided. Please specify an T1."
    
    if 'T2' in request.args:
        T2 = int(request.args['T2'])
    else:
        return "Error: No T2 field provided. Please specify an T2."
    
    if 'N_Biop' in request.args:
        N_Biop = int(request.args['N_Biop'])
    else:
        return "Error: No N_Biop field provided. Please specify an N_Biop... *Unknown (99)?*"
    
    if 'HypPlas' in request.args:
        HypPlas = int(request.args['HypPlas'])
    else:
        return "Error: No HypPlas field provided. Please specify an HypPlas... *Unknown (99)?*"
     
    if 'AgeMen' in request.args:
        AgeMen = int(request.args['AgeMen'])
    else:
        return "Error: No AgeMen field provided. Please specify an AgeMen."
    
    if 'Age1st' in request.args:
        Age1st = int(request.args['Age1st'])
    else:
        return "Error: No Age1st field provided. Please specify an Age1st."
    
    if 'N_Rels' in request.args:
        N_Rels = int(request.args['N_Rels'])
    else:
        return "Error: No N_Rels field provided. Please specify an N_Rels."
    
    if 'Race' in request.args:
        Race = int(request.args['Race'])
    else:
        return "Error: No Race field provided. Please specify an Race."


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

    ##########################################
    # os.environ['R_HOME'] = '/path/to/local/R/'
    # Installing required packages
    # Not sure if we need this on Docker deploy?
    '''
    utils = rpackages.importr('utils')
    utils.chooseCRANmirror(ind=1) # <-- closest geographical location
    packages = ('BCRA') # <-- Set package name here
    utils.install_packages(StrVector(packages))
    '''
    ##########################################    
    # Load R Package for BCRA
    bcra = importr('BCRA')

    # Set BCRA Functions
    check_summary = bcra.check_summary
    #absolute_risk = bcra.absolute_risk
    #relative_risk = bcra.relative_risk
    #risk_summary = bcra.risk_summary

    # Convert to R dataframe
    pandas2ri.activate()
    r_dt = ro.conversion.py2rpy(df) # df is a pd.DataFrame object
    
    # ABSOLUTE RISK (DEV)
    # try:
    #    abs_risk_val = absolute_risk(data=r_dt))
    #    return abs_risk_val
    # except:
    #    print('failed to get absolute risk...')
    
    return jsonify(check_summary(r_dt).to_dict())

app.run()