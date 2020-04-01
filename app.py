from flask_cors import CORS
from flask import Flask
import services as SE

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ------------------- AUTHENTICATION ----------------------------
@app.route('/api/login')
def login():
    return SE.authenticated()


# ------------------- DICTIONARY ----------------------------
@app.route('/api/mw/<word>')
def merriamWebster(word):
    return SE.merriamWebster(word=word)


@app.route('/api/gd/<word>')
def googleDictionary(word):
    return SE.googleDictionary(word=word)


@app.route('/api/ox/<word>')
def oxford(word):
    return SE.oxford(word=word)


# ------------------- TRANSLATOR ----------------------------
@app.route('/api/trans/<destLanguage>/<word>')
def translateWordWithDest(destLanguage, word):
    return SE.translateWordWithDest(destLanguage=destLanguage, word=word)


@app.route('/api/trans/<word>')
def translateWord(word):
    return SE.translateWord(word=word)


# ------------------- FAVOURITE ----------------------------
@app.route('/api/add/favourite/<word>')
def addFavouriteWord(word):
    return SE.addFavouriteWord(word=word)


@app.route('/api/get/favourite')
def getFavouriteWords():
    return SE.getFavouriteWords()


@app.route('/api/delete/favourite/<word>')
def deleteFavouriteWord(word):
    return SE.deleteFavouriteWord(word=word)


# ------------------- HISTORY ----------------------------
@app.route('/api/add/history/<word>')
def addHistoryWord(word):
    return SE.addHistoryWord(word=word)


@app.route('/api/get/history')
def getHistoryWords():
    return SE.getHistoryWords()


@app.route('/api/delete/history/<word>')
def deleteHistoryWord(word):
    return SE.deleteHistoryWord(word=word)


# ------------------- HOME ----------------------------
@app.route('/api/add/home/<word>')
def addHomeWord(word):
    return SE.addHomeWord(word=word)


@app.route('/api/get/home')
def getHomeWords():
    return SE.getHomeWords()


@app.route('/api/delete/home/<word>')
def deleteHomeWord(word):
    return SE.deleteHomeWord(word=word)


# ------------------- ERROR ----------------------------
@app.errorhandler(404)
def notFount(error):
    return error
    # return "We will come back soon..."


if __name__ == "__main__":
    app.run(debug=True)
