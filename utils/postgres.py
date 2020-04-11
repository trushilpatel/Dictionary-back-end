import json
import psycopg2
from os import getenv


class PostGress:
    def __init__(self, localhost, port, database, user, password):
        try:
            if getenv('PROD') == 'True':
                self.conn = psycopg2.connect(getenv("DB_URI"))
            else:
                self.conn = psycopg2.connect(host=localhost, port=port, database=database, user=user, password=password)
        except:
            print("error during connecting to the database")
        finally:
            self.cur = self.conn.cursor()
            print("connected to Database...")

    def __del__(self):
        self.conn.close()

    def createTables(self):
        pass
        """
        id serial not null , username unique varchar not null,  '
        'password varchar not null );')
        'create table oxford_words (word varchar unique not null,definition varchar not null);')
        'create table mwl_words (word varchar unique not null,definition varchar not null);')
        'create table favourite_words(user_id int Not Null, word varchar Unique Not null, foreign key(user_id)'
        references users(id));'
        create table history_words(user_id int Not Null, word varchar Unique Not null, foreign key(user_id)'
        references users(id));'
        """

    def login(self, username, password):
        execute = self.cur.execute("""select id from users where users.username = %s and users.password = %s""",
                                   (username, password))
        return {
            'userexist': bool(len(self.cur.fetchall()))
        }

    def getUserId(self, username):
        self.cur.execute("""select id from users where users.username = %s""", (username,))
        return self.cur.fetchall()[0][0]

    # check word existence
    def checkWordExistInDictionary(self, word, dictionary):
        self.cur.execute("""select * from {} where word = %s""".format(dictionary), (word,))
        return self.cur.fetchall()

    def getWordFromOxfordDictionary(self, word):
        word = self.checkWordExistInDictionary(word=word, dictionary='oxford_words')
        if len(word) == 0:
            return False
        return word[0][1]

    def getWordFromMWLDictionary(self, word):
        word = self.checkWordExistInDictionary(word=word, dictionary='mwl_words')
        if len(word) == 0:
            return False
        return word[0][1]

    # insert word and definition
    def insertWordInDictionary(self, word, word_definition, dictionary):
        try:
            self.cur.execute("""insert into {} (word, definition) values (%s, %s)""".format(dictionary),
                             (word, json.dumps(word_definition))
                             )
            self.conn.commit()
        except Exception as e:
            print(e)
            pass

    def insertWordInMWLDictionary(self, word, wordDefinition):
        self.insertWordInDictionary(
            word=word,
            word_definition=wordDefinition,
            dictionary='mwl_words'
        )

    def insertWordInOxfordDictionary(self, word, wordDefinition):
        self.insertWordInDictionary(
            word=word,
            word_definition=wordDefinition,
            dictionary='oxford_words'
        )

    # insert word into favourite or history
    def insertWord(self, word, username, tableName):
        try:
            self.cur.execute("""insert into {} (user_id, word) values (%s, %s)""".format(tableName),
                             (str(self.getUserId(username)), word))
            self.conn.commit()
        except Exception as e:
            print(e)
            pass

    def insertFavouriteWord(self, word, username):
        self.insertWord(word=word, username=username, tableName='favourite_words')

    def insertHistoryWord(self, word, username):
        self.insertWord(word=word, username=username, tableName='history_words')

    def insertHomeWord(self, word, username):
        return self.insertWord(word=word, username=username, tableName='home_words')

    # get favourite and history words
    def getWords(self, username, tableName):
        try:
            self.cur.execute("""select word from {} where user_id = %s""".format(tableName),
                             (str(self.getUserId(username)),)
                             )
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            pass

    def getHistoryWords(self, username):
        return self.getWords(username=username, tableName='history_words')

    def getFavouriteWords(self, username):
        return self.getWords(username=username, tableName='favourite_words')

    def getHomeWords(self, username):
        return self.getWords(username=username, tableName='home_words')

    # delete favourite and History Words
    def deleteWord(self, word, username, tableName):
        try:
            self.cur.execute("""delete from {} where user_id = %s and word = %s""".format(tableName),
                             (str(self.getUserId(username)), word)
                             )
            self.conn.commit()
        except Exception as e:
            print(e)
            pass

    def deleteHistoryWord(self, word, username):
        return self.deleteWord(word=word, username=username, tableName='history_words')

    def deleteFavouriteWord(self, word, username):
        return self.deleteWord(word=word, username=username, tableName='favourite_words')

    def deleteHomeWord(self, word, username):
        return self.deleteWord(word=word, username=username, tableName='home_words')

    def isFHWord(self, word, username, tableName):
        try:
            self.cur.execute("""select word from {} where user_id = %s and word = %s""".format(tableName),
                             (str(self.getUserId(username)), word)
                             )
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            pass

    def isFavouriteWord(self, word, username):
        favouriteWord = bool(self.isFHWord(word=word, username=username, tableName='favourite_words'))
        if favouriteWord is True:
            return True
        return False

    def isHomeWord(self, word, username):
        homeWord = bool(self.isFHWord(word=word, username=username, tableName='home_words'))
        if homeWord is True:
            return True
        return False
