from requests import get


class MerriamWebster:
    def __init__(self, mwl_api_key, mwd_api_key):
        self.mwl_api_key = mwl_api_key
        self.mwd_api_key = mwd_api_key

    def createLearnersUrl(self, word):
        url = "https://www.dictionaryapi.com/api/v3/references/learners/json/" \
              + word + "?key=" + self.mwl_api_key
        return url

    def createDictionaryUrl(self, word):
        url = "https://dictionaryapi.com/api/v3/references/collegiate/json/" \
              + word + "?key=" + self.mwd_api_key
        return url

    def getRequest(self, word):
        rLearner = get(self.createLearnersUrl(word=word))
        # rDictionary = get(self.createDictionaryUrl(word=word))

        return {
            'MWL': rLearner.json(),
            # 'MWD': rDictionary.json()
        }
