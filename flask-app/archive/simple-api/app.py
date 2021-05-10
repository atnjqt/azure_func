import flask
from flask import request, jsonify
import pandas as pd


app = flask.Flask(__name__)
app.config["DEBUG"] = True


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World --> ATN!<h1><p>Testing API on http://0.0.0.0:5000/api/example_df for df to R script ...'

@app.route('/atn', methods=['GET'])
def home():
    return "<h1>Python API Example for GET Request</h1><p>This site is a prototype API by ATN ...</p>"


@app.route('/api/example_df', methods=['GET'])
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
        return "Error: No N_Biop field provided. Please specify an N_Biop... *Can this be unknown (99)?*"
    
    if 'HypPlas' in request.args:
        HypPlas = int(request.args['HypPlas'])
    else:
        return "Error: No HypPlas field provided. Please specify an HypPlas... *Can this be unknown (99)?*"
     
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


    # Create dataframe from columns provided:
    df = pd.DataFrame({'id':PID,
              'T1':T1,
              'T2':T2,
              'N_Biop':N_Biop,
              'HypPlas':HypPlas,
              'AgeMen':AgeMen,
              'Age1st':Age1st,
              'N_Rels':N_Rels,
              'Race':Race},index=['id'])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.




    return jsonify(df.to_dict())

app.run()