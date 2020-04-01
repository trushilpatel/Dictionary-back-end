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
print(getenv('PG_PASSWORD'))
PG = PostGress(
    localhost=getenv('PG_LOCALHOST'),
    port=getenv('PG_PORT'),
    database=getenv('PG_DATABASE'),
    user=getenv('PG_USER'),
    password=getenv('PG_PASSWORD')
)
GD = GoogleDictionary()
MW = MerriamWebster(
    mwl_api_key=getenv('MWL_API_KEY'),
    mwd_api_key=getenv('MWD_API_KEY')
)
OX = Oxford(
    app_id=getenv('OX_APP_ID'),
    app_key=getenv('OX_APP_KEY')
)
TRA = Translate()


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


def authenticated():
    try:
        username = request.headers['username']
        password = request.headers['password']
        return PG.login(username, password)
    except:
        return {
            'error': "Login error check your username and password"
        }


def addFavouriteWord(word):
    PG.insertFavouriteWord(
        word=word,
        username=request.headers['username']
    )


def addHistoryWord(word):
    PG.insertFavouriteWord(
        word=word,
        username=request.headers['username']
    )


def translateWordWithDest(destLanguage, word):
    return TRA.translate(destLanguage=destLanguage, word=word)


def translateWord(word):
    return TRA.translate(word=word)


def getHistoryWords():
    return PG.getHistoryWords(username=request.headers['username'])


def deleteFavouriteWord(word):
    pass


def deleteHistoryWord(word):
    pass
