from flask import Flask, request, session, jsonify, render_template
import os
import requests
import json
# import pusher
import httplib2
import json
import urllib.request
from konlpy.tag import Okt
from collections import Counter
import pymysql
from datetime import datetime
import os
import sys
import urllib.request

h = httplib2.Http()
okt = Okt()

app = Flask(__name__)

# channels_client = pusher.Pusher(
#   app_id='870917',
#   key='777da506507b1625a6b2',
#   secret='8e40e4da9fddae82b42d',
#   cluster='ap3',
#   ssl=True
# )

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
  message = request.form['message']

  trans = papago(message) # 파파고 번역

  response = ""

  response += """
    <div class="chat-bubble result">
      <span class="chat-content">
        {0}
      </span>
      <img class="insert" src="/static/insert.png" onclick="goPara('{0}')"/>
    </div>
  """.format(trans)

  response_text = {"message":  message, "result": response}

  return jsonify(response_text)

def papago(message): # 파파고 번역

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


# run Flask app
if __name__ == "__main__":
  app.run()