import json

class MWU():
    def __init__(self):
        self.MWU = json.load(open('tmp/MWU.json', 'r', encoding='UTF8'))
        self.keys = [key for key in self.MWU]

    def useMWU(self, sentence):
        wordlist = []
        for word in self.keys:
            if word in sentence:
                wordlist.append(sentence.replace(word, self.MWU[word]))
        
        return wordlist[:5]


if __name__ == "__main__":
    w = MWU()
    print(w.useMWU("I want to get there as well."))