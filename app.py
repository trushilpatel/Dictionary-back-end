import config
from os import getenv
from flask_cors import CORS
from flask import Flask, request
from utils.oxford import Oxford
from utils.merriamWebster import MerriamWebster
from utils.google import GoogleDictionary
from utils.translate import Translate
from utils.mongoDB import DataBaseUtility

# commonly used objects
MOD = DataBaseUtility(atlas_link=getenv("ATLAS_LINK"), databaseName=getenv("DATABASE_NAME"))
GD = GoogleDictionary()
MW = MerriamWebster(mwl_api_key=getenv('MWL_API_KEY'), mwd_api_key=getenv('MWD_API_KEY'))
OX = Oxford(app_id=getenv('OX_APP_ID'), app_key=getenv('OX_APP_KEY'))
TRA = Translate()

# app configuration
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# routes
@app.route('/login', methods=["POST"])
def login():
    return MOD.login(request.json['username'], request.json['password'])


@app.route('/api/mw/<word>')
def merriamWebster(word):
    return MW.getRequest(word)


@app.route('/api/gd/<word>')
def googleDictionary(word):
    return GD.getRequest(word)


@app.route('/api/ox/<word>')
def oxford(word):
    # return "We will back soon..."
    return OX.getRequest(word)


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
