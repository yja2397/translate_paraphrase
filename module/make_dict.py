# A very rudimentary article spinner using trigrams.

import nltk
import random
import numpy as np
from bs4 import BeautifulSoup
import json
import pandas as pd

###############################################
# want to collect data by txt file

# data collected by COCA - NEW data, TV data, movie data, soap data.
# @ @ @ @ @ -> PLAYOR - in tv_text.txt, movies_text, soap-text
# new_text = BeautifulSoup(open('tmp/new_text.txt', encoding='UTF-8').read())
# corpora = new_text.findAll('review_text')

# tv_text = BeautifulSoup(open('tmp/tv_text.txt', encoding='UTF-8').read())
# corpora += tv_text.findAll('review_text')

# movies_text = BeautifulSoup(open('tmp/movies_text.txt', encoding='UTF-8').read())
# corpora += movies_text.findAll('review_text')

# soap_text = BeautifulSoup(open('tmp/soap-text.txt', encoding='UTF-8').read())
# corpora += soap_text.findAll('review_text')

###########################################################

## Want to collect by csv file
# # data collected by twitter, http://data.world 

# # my favorite data
# favorite = pd.read_csv('tmp/favorite_tweets.csv')
# favorite = favorite[["text"]]

# # Twitter User Data
# user_data = pd.read_csv('tmp/twitter_user_data.csv')
# user_data = user_data[["text"]]

# corpora = favorite + user_data

# extract trigrams and insert into dictionary
# (w1, w3) is the key, [ w2 ] are the values
trigrams = {}
# for review in corpora:
#     s = review.text.lower()
for review in corpora["text"]:
    if isinstance(review, float):
        pass
    else:
        s = review.lower()
        tokens = nltk.tokenize.word_tokenize(s)
        for i in range(len(tokens) - 2):
            if type(tokens[i]) == str and type(tokens[i+2]) == str:
                k = (tokens[i], tokens[i+2])
                if k not in trigrams:
                    trigrams[k] = []
                trigrams[k].append(tokens[i+1])


# turn each array of middle-words into a probability vector
trigram_probabilities = {}
for k, words in trigrams.items():
    # create a dictionary of word -> count
    if len(set(words)) > 1:
        # only do this when there are different possibilities for a middle word
        d = {}
        n = 0
        for w in words:
            if w not in d:
                d[w] = 0
            d[w] += 1
            n += 1
        for w, c in d.items():
            d[w] = float(c) / n
        trigram_probabilities[k] = d

with open("tmp/twitter.json", "w") as f:
    k = trigram_probabilities.keys() 
    v = trigram_probabilities.values() 
    k1 = [str(i) for i in k]
    json.dump(json.dumps(dict(zip(*[k1,v]))),f) 

