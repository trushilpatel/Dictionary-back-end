import config
from os import getenv
from flask_cors import CORS
from flask import Flask
from utils.oxford import Oxford
from utils.merriamWebster import MerriamWebster
from utils.google import GoogleDictionary
from utils.translate import Translate

# commonly used objects
GD = GoogleDictionary()
MW = MerriamWebster(getenv('MWL_API_KEY'), getenv('MWD_API_KEY'))
OX = Oxford(getenv('OX_APP_ID'), getenv('OX_APP_KEY'))
TRA = Translate()

# app configuration
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# routes
@app.route('/api/mw/<word>')
def merriamWebster(word):
    return MW.getRequest(word)


@app.route('/api/gd/<word>')
def googleDictionary(word):
    return GD.getRequest(word)


@app.route('/api/ox/<word>')
def oxford(word):
    return "We will back soon..."  # OX.getRequest(word)


@app.route('/api/trans/<destLanguage>/<word>')
def translateWordWithDest(destLanguage, word):
    return TRA.translate(destLanguage=destLanguage, word=word)


@app.route('/api/trans/<word>')
def translateWord(word):
    return TRA.translate(word=word)


@app.errorhandler(404)
def notFount(e):
    return "We will come back soon..."


if __name__ == "__main__":
    app.run(debug=True)
