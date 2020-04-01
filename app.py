from flask_cors import CORS
from flask import Flask
import services as SE

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/login')
def login():
    print('hello')
    return SE.authenticated()


@app.route('/api/mw/<word>')
def merriamWebster(word):
    return SE.merriamWebster(word=word)


@app.route('/api/gd/<word>')
def googleDictionary(word):
    return SE.googleDictionary(word=word)


@app.route('/api/ox/<word>')
def oxford(word):
    return SE.oxford(word=word)


@app.route('/api/trans/<destLanguage>/<word>')
def translateWordWithDest(destLanguage, word):
    return SE.translateWordWithDest(destLanguage=destLanguage, word=word)


@app.route('/api/trans/<word>')
def translateWord(word):
    return SE.translateWord(word=word)


@app.route('/api/add/favourite/<word>')
def addFavouriteWord(word):
    SE.addFavouriteWord(word=word)


@app.route('/api/add/history/<word>')
def addHistoryWord(word):
    SE.addHistoryWord(word=word)


@app.route('/api/delete/favourite/<word>')
def deleteFavouriteWord(word):
    SE.deleteFavouriteWord(word=word)


@app.route('/api/delete/history/<word>')
def deleteHistoryWord(word):
    SE.deleteHistoryWord(word=word)


@app.route('/api/get/history_words')
def getHistoryWords():
    return SE.getHistoryWords()


@app.route('/api/get/favourite_words')
def getFavouriteWords():
    return SE.getFavouriteWords()


@app.errorhandler(404)
def notFount(error):
    return error
    # return "We will come back soon..."


if __name__ == "__main__":
    app.run(debug=True)
