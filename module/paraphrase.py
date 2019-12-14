import urllib.request
import json
import time
from module import wordnetSimilarity
from module import toknize
from module import biset
from module import article_spinner
from module import MWU

class paraphrase():
    def isEnglishOrKorean(self, input_s):
        k_count = 0
        e_count = 0
        for c in input_s:
            if ord('가') <= ord(c) <= ord('힣'):
                k_count+=1
            elif ord('a') <= ord(c.lower()) <= ord('z'):
                e_count+=1
        return "k" if k_count>1 else "e"

    def papago(self, message, source="ko"): # 파파고 번역

        client_id = "daFbPHQo9YDVHRyjaPgy"
        client_secret = "P6qPCamZnK"
        # 클라이언트 id와 secret

        if(source == "ko"):
            target = "en"
        else:
            target = "ko"
        
        encText = urllib.parse.quote(message)
        data = "source="+source+"&target="+target+"&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()    
            res = response_body.decode('utf-8')
            i = json.loads(res)
            print(i)

            return i['message']['result']['translatedText']
        else:
            return "Error Code:" + rescode
    
    def wordnet(self, message):
        wS = wordnetSimilarity.wordnet()
        return wS.paraPhraseThisSentence(message)

    def tokin(self, message):
        tk = toknize.token()
        return tk.paraPhraseThisSentence(message)

    def bisets(self, message):
        bs = biset.biset()
        return bs.bisetData(message)

    def COCA(self, message):
        tri = article_spinner.trigram()
        return tri.list_COCA(message) + tri.list_twitter(message)

    # def twitter(self, message):
    #     tri = article_spinner.trigram()
    #     return tri.list_twitter(message)
    
    def MWU(self, message):
        mwu = MWU.MWU()
        return mwu.useMWU(message)

    def makeResult(self, message):
        start = time.time()
        if self.isEnglishOrKorean(message) == "k": # 한국어일 때
            message = self.papago(message) # 번역
        print("translate : " + str(time.time() - start))
        start = time.time()
        mM = self.MWU(message) # MWU에서 추출한 비슷한 문장
        print("MWU : " + str(time.time() - start))
        start = time.time()
        mR = self.wordnet(message) # wordnet에서 추출한 비슷한 문장들
        print("wordnet : " + str(time.time() - start))
        start = time.time()
        mC = self.COCA(message) # COCA 사용한 비슷한 문장들
        print("COCA : " + str(time.time() - start))
        # start = time.time()
        # mT = self.twitter(message) # twitter 사용한 비슷한 문장들
        # print("TWITTER : " + str(time.time() - start))
        start = time.time()
        mB = self.bisets(message) # DB에서 추출한 비슷한 문장들
        print("DB : " + str(time.time() - start))
        start = time.time()
        # mS = self.tokin(message) # 동의어를 이용한 비슷한 문장들
        
        result = [message] # 번역된 것
        result += mM + mR + mC + mB # + mS

        return result

    def processResult(self, message):
        result = self.makeResult(message)

        finalResult = []
        for final in result:
            finalResult.append(final.replace("_"," ").replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!").replace(" ?", "?").replace(" i ", " I ").replace(" i'", " I'").replace(" n't", "n't"))

        result = finalResult

        if len(result) > 1:
            delete = []
            for i in range(1,len(result)):
                if result[i].count(' ') < message.count(' ') - 3: # 너무 단어 개수가 짧은 문장 제외
                    delete.append(i)
                elif result[0][:-3].lower().strip() in result[i].lower().strip(): # 중복제거
                    delete.append(i)
            
            delete.reverse()
            for i in delete:
                del result[i]

        return result
    
    def manyResult(self, message):

        return self.processResult(message)

# run Flask app
if __name__ == "__main__":
    translate = paraphrase()
    result = translate.papago("Android studios are too hard to learn.", source="en")
    print(result)