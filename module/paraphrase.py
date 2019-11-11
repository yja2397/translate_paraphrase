import urllib.request
import json
from module import wordnetSimilarity
from module import toknize
from module import biset
from module import article_spinner

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

    def papago(self, message): # 파파고 번역

        client_id = "daFbPHQo9YDVHRyjaPgy"
        client_secret = "P6qPCamZnK"
        # 클라이언트 id와 secret
        
        encText = urllib.parse.quote(message)
        data = "source=ko&target=en&text=" + encText
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
        return tri.list_COCA(message)

    def twitter(self, message):
        tri = article_spinner.trigram()
        return tri.list_twitter(message)
    
    def manyResult(self, message):
        if self.isEnglishOrKorean(message) == "k": # 한국어일 때
            message = self.papago(message) # 번역
        mB = self.bisets(message) # DB에서 추출한 비슷한 문장들
        mR = self.wordnet(message) # wordnet에서 추출한 비슷한 문장들
        mC = self.COCA(message) # COCA 사용한 비슷한 문장들
        mT = self.twitter(message) # twitter 사용한 비슷한 문장들
        mS = self.tokin(message) # 동의어를 이용한 비슷한 문장들
        
        result = [message] # 번역된 것
        result += mB + mR + mC + mT + mS
        result = list(set(result))
        return result


# run Flask app
if __name__ == "__main__":
    translate = paraphrase()
    result = translate.manyResult("Every man has a knack for rolling.")
    print(result)