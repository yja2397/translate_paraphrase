from module import db
from module.paraInterface import *

class biset(paraInterface):
    def __init__(self):
        self.db = db.Database()

    def synonymIfExists(self, sentence):
        words = []
        for (word, t) in self.tag(sentence):
            if self.paraphraseable(t) and word not in ["i","I"]:
                # print(word)
                words.append(word)
        
        return words

    def bisetData(self, sentence):
        synonym = self.synonymIfExists(sentence)
        length = len(synonym)
        if length > 0:
            words = "'%%" + synonym[0] + "%%'"
            if length > 1:
                for i in range(1,length):
                    words += " and meaning like "
                    words += "'%%" + synonym[i] + "%%'"

            sql     = "select sentence from TS.idiom where meaning like " + words

            data = self.db.executeAll(sql)
            self.db.commit()

            if data:
                words = []
                for i in data:
                    words.append(i['sentence'].replace('\xa0', ' '))

                return words
            else:
                return []
        else:
            resturn []

# run Flask app
if __name__ == "__main__":
    translate = biset()
    translate.bisetData("Every man has a knack for rolling.")


