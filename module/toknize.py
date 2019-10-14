from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from random import randint
from module.paraInterface import *

class token(paraInterface):
    def synonyms(self, word, tag):
        lemma_lists = [ss.lemmas() for ss in wn.synsets(word, self.pos(tag))]
        lemmas = [lemma.name() for lemma in sum(lemma_lists, [])]
        return set(lemmas)

    def synonymIfExists(self, sentence):
        for (word, t) in self.tag(sentence):
            if self.paraphraseable(t):
                syns = self.synonyms(word, t)
                if syns:
                    if len(syns) > 1:
                        yield [word, list(syns)]
                        continue
            yield [word, []]
