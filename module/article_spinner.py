# A very rudimentary article COCA using trigrams.

# @ @ @ @ @ -> PLAYOR - in tv_text.txt
import nltk
import random
import numpy as np
from bs4 import BeautifulSoup
import json

class trigram():
    def __init__(self):
        with open("tmp/COCA.json") as f:
            data = json.load(f)
            dic = json.loads(data)
            k = dic.keys() 
            v = dic.values() 
            k1 = [eval(i) for i in k] 
            self.COCA = dict(zip(*[k1,v])) 

        with open("tmp/twitter.json") as f:
            data = json.load(f)
            dic = json.loads(data)
            k = dic.keys() 
            v = dic.values() 
            k1 = [eval(i) for i in k] 
            self.twitter = dict(zip(*[k1,v])) 


    def random_sample(self, d):
        # choose a random sample from dictionary where values are the probabilities
        r = random.random()
        cumulative = 0
        for w, p in d.items():
            cumulative += p
            if r < cumulative:
                return w

    def make_COCA(self, review):

        s = review.lower()
        tokens = nltk.tokenize.word_tokenize(s)
        for i in range(len(tokens) - 2):
            if random.random() < 0.2: # 20% chance of replacement
                k = (tokens[i], tokens[i+2])
                if k in self.COCA:
                    w = self.random_sample(self.COCA[k])
                    tokens[i+1] = w
        mystr = " ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!").replace(" ?", "?").replace(" i ", " I ")
        return mystr.capitalize()

    def list_COCA(self, review):
        result = []

        for i in range(0, 5): # 최대 5개, 최소 0개의 결과물.
            text = self.make_COCA(review)
            if text != review:
                result.append(text)

        return list(set(result))

    def make_twitter(self, review):

        s = review.lower()
        tokens = nltk.tokenize.word_tokenize(s)
        for i in range(len(tokens) - 2):
            if random.random() < 0.2: # 20% chance of replacement
                k = (tokens[i], tokens[i+2])
                if k in self.twitter:
                    w = self.random_sample(self.twitter[k])
                    tokens[i+1] = w
        mystr = " ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!").replace(" ?", "?").replace(" i ", " I ")
        return mystr.capitalize()

    def list_twitter(self, review):
        result = []

        for i in range(0, 5): # 최대 5개, 최소 0개의 결과물.
            text = self.make_twitter(review)
            if text != review:
                result.append(text)

        return list(set(result))

if __name__ == '__main__':
    print(trigram().list_COCA("I went to park, I want it"))
    print(trigram().list_twitter("I went to park, I want it"))
