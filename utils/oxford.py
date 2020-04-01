from requests import get
import json


class Oxford:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.language = 'en'

    def createUrl(self, word):
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' \
              + self.language + '/' + word.lower()
        return url

    def getRequest(self, word):
        r = get(self.createUrl(word=word), headers={'app_id': self.app_id,
                                                    'app_key': self.app_key
                                                    }
                )
        return r.json()

