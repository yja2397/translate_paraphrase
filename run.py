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

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/index.html', methods=['GET', 'POST'])
def index2():
  return render_template('index.html')

@app.route('/para.html', methods=['GET', 'POST'])
def para():
  return render_template('para.html')

@app.route('/sen.html', methods=['GET', 'POST'])
def sen():
  return render_template('sen.html')

@app.route('/login.html', methods=['GET', 'POST'])
def log():
  return render_template('login.html')

@app.route('/join.html', methods=['GET', 'POST'])
def joi():
  return render_template('join.html')

@app.route('/translate', methods=['POST'])
def trans():
  message = request.form['message']

  tr = translate.translate()
  trans = tr.papago(message) # 파파고 번역

  transSet = trans.replace("'", "\\'")

  response = ""

  response += """
    <div class="chat-bubble result">
      <span class="chat-content">
        {0}
      </span>
      <img class="insert" src="/static/insert.png" onclick='goPara("{1}")'/>
    </div>
  """.format(trans, transSet)

  response_text = {"message":  message, "result": response}

  return jsonify(response_text)


@app.route('/insert', methods=['POST'])
def insert():
  message = request.form['message']

  db_class = db.Database()

  sql     = """SELECT sentence FROM TS.sentence WHERE sentence = '%s'"""% (message)
  data = db_class.executeOne(sql)

  if not data:
    sql     = """INSERT INTO TS.sentence(sentence) \
                VALUES('%s')"""% (message)
    db_class.execute(sql)

  sql     = """UPDATE TS.sentence \
              SET searchCnt = searchCnt + 1 \
              WHERE sentence='%s'"""% (message)
  db_class.execute(sql)

  db_class.commit()

  if session['logged_in']: # login한 사용자는 저장.
    mM = user.memberManage()

    mM.insertSen(message, session['userid'])

  return 'commit'

@app.route('/login', methods=['POST'])
def login():
  userid = request.form['userid']
  pswd = request.form['pswd'] 

  mM = user.memberManage()
  connect = mM.login(userid, pswd)

  if connect == 0:
    session['logged_in'] = True
    session['userid'] = userid
    session['pswd'] = pswd

  response_text = {"connect": connect, "id" : userid}

  return jsonify(response_text)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
  session['logged_in'] = False

  return 'logout'
  

@app.route('/join', methods=['POST'])
def join():
  userid = request.form['userid']
  pswd = request.form['pswd'] 

  mM = user.memberManage()
  connect = mM.join(userid, pswd)

  if connect == 0:
    connect = mM.login(userid, pswd)
    session['logged_in'] = True
    session['userid'] = userid
    session['pswd'] = pswd
  
  response_text = {"connect":  connect, "id" : userid}

  return jsonify(response_text)
  

# run Flask app
if __name__ == "__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run()