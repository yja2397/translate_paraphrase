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
import sys

from module import db # db
from module import user
from module import translate

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

  tr = translate.translate()
  trans = tr.papago(message) # 파파고 번역

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

  return

@app.route('/login', methods=['POST'])
def login():
  userid = session.form['id']
  pswd = session.form['pswd'] 

  mM = user.memberManage()
  connect = mM.login(userid, pswd)

  if connect == 1:
    response_text = {"alert" : "잘못된 아이디입니다."}
  elif connect == 2:
    response_text = {"alert" : "비밀번호가 잘못되었습니다."}
  else:
    response_text = {"alert" : "환영합니다. " + connect + "님."}
  
  return jsonify(response_text)

@app.route('/join', methods=['POST'])
def join():
  userid = session.form['id']
  pswd = session.form['pswd'] 

  mM = user.memberManage()
  connect = mM.join(userid, pswd)

  if connect == 0:
    response_text = {"alert" : "회원가입이 성공적으로 진행되었습니다.\n 자동 로그인됩니다."}
  else:
    response_text = {"alert" : "이미 등록된 아이디입니다."}

  return jsonify(response_text)
  

# run Flask app
if __name__ == "__main__":
  app.run()