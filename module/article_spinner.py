# A very rudimentary article spinner using trigrams.

# @ @ @ @ @ -> PLAYOR - in tv_text.txt
import nltk
import random
import numpy as np
from bs4 import BeautifulSoup
import json

class trigram():
    def __init__(self):
        with open("tmp/trigram_probabilities.json") as f:
            data = json.load(f)
            dic = json.loads(data)
            k = dic.keys() 
            v = dic.values() 
            k1 = [eval(i) for i in k] 
            self.trigram_probabilities = dict(zip(*[k1,v])) 

    def random_sample(self, d):
        # choose a random sample from dictionary where values are the probabilities
        r = random.random()
        cumulative = 0
        for w, p in d.items():
            cumulative += p
            if r < cumulative:
                return w

    def test_spinner(self, review):
        # review = random.choice(corpora)
        s = review.lower()
        # print("Original:" +  s)
        tokens = nltk.tokenize.word_tokenize(s)
        for i in range(len(tokens) - 2):
            if random.random() < 0.2: # 20% chance of replacement
                k = (tokens[i], tokens[i+2])
                if k in self.trigram_probabilities:
                    w = self.random_sample(self.trigram_probabilities[k])
                    tokens[i+1] = w
        # print("Spun:")
        mystr = " ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!")
        mystr.capitalize()
        return mystr

# if __name__ == '__main__':
#     test_spinner()
#     test_spinner()
#     test_spinner()
