import urllib.request

class translate():
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