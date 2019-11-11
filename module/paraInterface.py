from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from random import randint

class paraInterface:
    # Function to tag sentence with part of speach
    def tag(self, sentence):
        words = word_tokenize(sentence)
        words = pos_tag(words)
        return words

    # Determine the POS to paraphrase
    def paraphraseable(self, tag):
        return tag.startswith('NN') or tag =='VB' or tag.startswith('JJ')

    # POS tagging
    def pos(self, tag):
        if tag.startswith('NN'):
            return wn.NOUN
        elif tag.startswith('V'):
            return wn.VERB

    # to to get synonums from wordnet nltk as well as from python dictonary synonums
    def synonymIfExists(self, sentence):
        return []

    # Function to get the semantic similar synonums and the total count of synonums in the entire sentence
    def paraphrase(self, sentence):
        bagOfWords = []
        counter = 1    
        for tempArray in self.synonymIfExists(sentence):
            eachBoW=[]
            eachBoW.append(tempArray[0])
            eachBoW.extend(tempArray[1])
            eachBoW=list(set(eachBoW))    
            counter *= len(eachBoW)
            bagOfWords.append(eachBoW)
        return bagOfWords,counter
    
    # Function to re-create sentence with synonums where the synonums are taken in randon order 
    def paraPhraseThisSentence(self, sentence):
        ppList = []
        vList,count = self.paraphrase(sentence)
        allWordsCount = len(vList)
        for y in range(count):
            str = []
            returnStr = " "
            for w in range(allWordsCount):
                # ading = vList[w][randint(0,len(vList[w])-1)] #.replace("_"," ")
                str.append(vList[w][randint(0,len(vList[w])-1)].replace("_"," ").replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!").replace(" ?", "?"))
                ppList.append(returnStr.join(str))
        ppList = list(set(ppList))
        return ppList