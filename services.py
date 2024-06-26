import json

import config
from os import getenv
from utils.oxford import Oxford
from utils.merriamWebster import MerriamWebster
from utils.google import GoogleDictionary
from utils.translate import Translate
from utils.postgres import PostGress
from flask import request

# commonly used objects
PG = PostGress(
    localhost=getenv('PG_LOCALHOST'),
    port=getenv('PG_PORT'),
    database=getenv('PG_DATABASE'),
    user=getenv('PG_USER'),
    password=getenv('PG_PASSWORD')
)
MW = MerriamWebster(mwl_api_key=getenv("MWL_API_KEY"), mwd_api_key=getenv("MWD_API_KEY"))
GD = GoogleDictionary()
OX = Oxford(
    app_id=getenv('OX_APP_ID'),
    app_key=getenv('OX_APP_KEY')
)
TRA = Translate()


# ------------------- AUTHENTICATION ----------------------------
def authenticated():
    try:
        username = request.headers['username']
        password = request.headers['password']
        return PG.login(username, password)
    except:
        return {
            'error': "Login error check your username and password"
        }


# ------------------- TRANSLATOR ----------------------------
def translateWordWithDest(destLanguage, word):
    return {
        'translation': TRA.translate(destLanguage=destLanguage, word=word),
        'home': PG.isHomeWord(word=word, username=request.headers['username']),
        'favourite': PG.isFavouriteWord(word=word, username=request.headers['username'])
    }


def translateWord(word):
    return {
            'translation':TRA.translate(word=word),
            'home': PG.isHomeWord(word=word, username=request.headers['username']),
            'favourite': PG.isFavouriteWord(word=word, username=request.headers['username'])
        }

# ------------------- DICTIONARY ----------------------------
def googleDictionary(word):
    return GD.getRequest(word)


def merriamWebster(word):
    definition = None
    wordDefinition = PG.getWordFromMWLDictionary(word)
    if wordDefinition is False:
        print('mw api to www')
        definition = MW.getRequest(word)
        PG.insertWordInMWLDictionary(word=word, wordDefinition=definition)
    else:
        try:
            definition = json.loads(wordDefinition)
        except:
            print("error in merriamWebster")
    return definition


def oxford(word):
    definition = None
    wordDefinition = PG.getWordFromOxfordDictionary(word)
    if wordDefinition is False:
        print('oxford api to www')
        definition = OX.getRequest(word)
        PG.insertWordInOxfordDictionary(word=word, wordDefinition=definition)
    else:
        try:
            definition = json.loads(wordDefinition)
        except:
            print("error in oxford")
    return definition


# ------------------- HISTORY ----------------------------
def addHistoryWord(word):
    PG.insertHistoryWord(
        word=word,
        username=request.headers['username']
    )
    return {"status": "successful"}


def getHistoryWords():
    return {
        'rows': PG.getHistoryWords(username=request.headers['username'])
    }


def deleteHistoryWord(word):
    PG.deleteHistoryWord(username=request.headers['username'], word=word)
    return {"status": "successful"}


# ------------------- FAVOURITE ----------------------------
def addFavouriteWord(word):
    PG.insertFavouriteWord(
        word=word,
        username=request.headers['username']
    )
    return {"status": "successful"}


def getFavouriteWords():
    return {
        'rows': PG.getFavouriteWords(username=request.headers['username'])
    }


def deleteFavouriteWord(word):
    PG.deleteFavouriteWord(username=request.headers['username'], word=word)
    return {"status": "successful"}


# ------------------- HOME ----------------------------
def addHomeWord(word):
    PG.insertHomeWord(
        word=word,
        username=request.headers['username']
    )
    return {"status": "successful"}


def getHomeWords():
    return {
        'rows': PG.getHomeWords(username=request.headers['username'])
    }


def deleteHomeWord(word):
    PG.deleteHomeWord(username=request.headers['username'], word=word)
    return {"status": "successful"}

