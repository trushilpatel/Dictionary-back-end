import json

from requests import get


class GoogleDictionary:
    def getRequest(self, word):
        url = "https://api.dictionaryapi.dev/api/v1/entries/en/" + word
        r = get(url)
        return {
            "gd": json.loads(r.text)
        }
