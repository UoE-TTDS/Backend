import nltk
from nltk import PorterStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = set(stopwords.words('english'))


class Preprocessor:
    def __init__(self, functions):
        self.functions = functions

    def preprocess(self, data):
        d = data.split()
        for f in self.functions:
            d = f(d)
        return d


class PreprocessorBuilder:

    def __init__(self):
        self.modules = []

    def stem(self):
        stemmer = PorterStemmer()

        def st(words):
            for word in words:
                yield stemmer.stem(word)

        self.modules.append(st)
        return self

    def stop_words(self):
        def remove(words):
            for word in words:
                if word not in stopwords:
                    yield word

        self.modules.append(remove)
        return self

    def to_lowercase(self):
        def low(words):
            for w in words:
                yield w.lower()

        self.modules.append(low)
        return self

    def smart_removal(self):
        substitutions = {}

        def remove(words):
            for w in words:
                for key in substitutions:
                    w = w.replace(key,substitutions[key])
                yield key
        self.modules.append(remove)
        return self

    def remove_special(self):
        special = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        def remove(words):
            for w in words:
                word = w
                for s in special:
                    word = word.replace(s, "")
                yield word

        self.modules.append(remove)
        return self

    def build(self):
        return Preprocessor(self.modules)
