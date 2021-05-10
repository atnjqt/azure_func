import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World --> ATN!'

@app.route('/atn', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()
