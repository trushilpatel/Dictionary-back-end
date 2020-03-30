from googletrans import Translator


class Translate:
    def __init__(self):
        self.translator = Translator()

    def EnglishToGujarati(self, word):
        return self.translator.translate(word, dest='gu').text

    def EnglishToHindi(self, word):
        return self.translator.translate(word, dest='hi').text

    def GujaratiToEnglish(self, word):
        return self.translator.translate(word, dest='en').text

    def HindiToEnglish(self, word):
        return self.translator.translate(word, dest='en').text

    def translate(self, word, destLanguage=None):

        """
        if destLanguage == 'gu':
            return {"English": self.GujaratiToEnglish(word)}
        elif destLanguage == 'hi':
            return {"English": self.HindiToEnglish(word)}
        else:
        """
        return {
            "English": self.HindiToEnglish(word),
            "Gujarati": self.EnglishToGujarati(word),
            "Hindi": self.EnglishToHindi(word)
        }


if __name__ == '__main__':
    translate = Translate()
    print(translate.translate(destLanguage='gu', word='પાટિયું'))
