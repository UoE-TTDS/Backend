import nltk
from nltk import PorterStemmer
from nltk.corpus import stopwords
import re

nltk.download('stopwords')
stopwords = set(stopwords.words('english'))


class Preprocessor:
    def __init__(self, functions):
        self.functions = functions

    def preprocess(self, data):
        data = data.lower()
        data = re.sub(r'[\[\(]\s*(verse|hook|chorus).*[\]\)]', ' ', data)  # remove special sub-cases
        data = re.sub(r"\w+('\w+)", ' ', data)  # remove contractions
        data = re.sub(r'[\W|\d+]', ' ', data)  # remove all punct marks and numbers, substitute with space
        data = re.sub(r'\s{2,}', ' ', data)  # convert multi-spaces to one space
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

    def build(self):
        return Preprocessor(self.modules)
