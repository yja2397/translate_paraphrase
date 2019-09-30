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

from module import db # db

h = httplib2.Http()
okt = Okt()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/index.html')
def index2():
  return render_template('index.html')

@app.route('/para.html')
def para():
  return render_template('para.html')

@app.route('/sen.html')
def sen():
  return render_template('sen.html')

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

@app.route('/insert', methods=['POST'])
def insert():
  message = request.form['message']

  db_class = db.Database()

  sql     = "SELECT sentence FROM TS.sentence WHERE sentence = '%s'"% (message)
  data = db_class.executeOne(sql)

  if not data:
    sql     = "INSERT INTO TS.sentence(sentence) \
                VALUES('%s')"% (message)
    db_class.execute(sql)

  sql     = "UPDATE TS.sentence \
              SET searchCnt = searchCnt + 1 \
              WHERE sentence='%s'"% (message)
  db_class.execute(sql)

  db_class.commit()

 

# run Flask app
if __name__ == "__main__":
  app.run()