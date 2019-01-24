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
        data = re.sub(r'[\W|\d+]', ' ', data)  # remove all punct marks and numbers, substitute with space
        data = re.sub(r'\s{2,}', ' ', data)   # convert multi-spaces to one space
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

    def number_removal(self):
        def remove(words):
            for w in words:
                try:
                    float(w)  # removed as digit
                except ValueError:
                    yield w
        self.modules.append(remove)
        return self

    def regex_removal(self):
        import re
        rgx = [
            "[\[\(]\s*(hook|chorus).*[\]\)]"
        ]
        rgx = [re.compile(r) for r in rgx]
        def remove(words):
            for w in words:
                for r in rgx:
                    if r.match(w):
                        continue
                    else:
                        yield w
        self.modules.append(remove)
        return self

    def smart_removal(self):
        substitutions = {
            "I'm" : "I am"  # will be removed with stopwords
        }

        def remove(words):
            for w in words:
                for key in substitutions:
                    w = w.replace(key, substitutions[key])
                yield w
        self.modules.append(remove)
        return self

    def remove_special(self):
        special = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" # removed as punc mark

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
