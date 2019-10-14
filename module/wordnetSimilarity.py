from nltk.corpus import wordnet as wn
from sematch.semantic.similarity import WordNetSimilarity
from vocabulary.vocabulary import Vocabulary as vb
import json
from random import randint
import spacy
import os.path
from module.paraInterface import *

nlp = spacy.load('en_core_web_sm')

class wordnet(paraInterface):
    # Function to crate synonyms using wordnet nltk
    def synonyms(self, word, tag):
        listOfLemmas = [baseWord.lemmas() for baseWord in wn.synsets(word, self.pos(tag))]  
        if len(listOfLemmas) > 0:
            listOfLemmas = listOfLemmas[0]
            lemmas = [lemma.name() for lemma in listOfLemmas]
            return set(lemmas)
        else:
            return set([])

    # Create  dictonary synonums
    def dictonarySynonums(self, word):
        synJSON = vb.synonym(word)
        if synJSON != False:
            synonyms_lists = [dictSyno["text"].encode('ascii', 'ignore') for dictSyno in json.loads(vb.synonym(word))]
            return set(synonyms_lists)
        else:
            return set([])

    # controll set to calculate the semantic similarity of synonums from the base words using SPACY
    def controlledSetSpacy(self, word, similarWords):
        utf_en_word = nlp(word.decode('utf-8', 'ignore'))
        for similarWord in similarWords.copy():
            utf_en_similarWord = nlp(similarWord.decode('utf-8','ignore'))
            if utf_en_word.similarity(utf_en_similarWord) <.76: # Variable to control accuracy of controlset 
                similarWords.discard(similarWord)
        return similarWords

    # controll set to calculate the semantic similarity of synonums from the base words using WordNetSimilarity
    def controlledSetWordNetSimilarity(self, word, similarWords):
        wns = WordNetSimilarity()
        for similarWord in similarWords.copy():
            if wns.word_similarity(word, similarWord, 'li') < 0.9996: # Variable to control accuracy of controlset
                similarWords.discard(similarWord)
        return similarWords

    # to to get synonums from wordnet nltk as well as from python dictonary synonums
    def synonymIfExists(self, sentence):
        for (word, t) in self.tag(sentence):
            if self.paraphraseable(t) and word not in ["i","I"]:
                syns = self.synonyms(word, t)
                syns.update(self.dictonarySynonums(word))
                if syns:
                    syns = self.controlledSetWordNetSimilarity(word,syns) # Or use the commented controlled set
                    #syns = controlledSetSpacy(word,syns)
                    if len(syns) > 1:
                        yield [word, list(syns)]
                        continue
                    else:
                        yield [word,[]]
                else:
                    yield [word,[]]
            else:
                yield [word,[]]
