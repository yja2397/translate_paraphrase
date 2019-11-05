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
from gtts import gTTS
from time import sleep
import pyglet

from module import db # db
from module import user
from module import paraphrase

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
    mM = user.memberManage()
    rows = mM.findPara(session['userid'])
    return render_template('para.html', rows=rows)

@app.route('/sen.html', methods=['GET', 'POST'])
def sen():
    mM = user.memberManage()
    rows = mM.findSen(session['userid'])
    return render_template('sen.html', rows=rows)

@app.route('/login.html', methods=['GET', 'POST'])
def log():
    return render_template('login.html')

@app.route('/join.html', methods=['GET', 'POST'])
def joi():
    return render_template('join.html')

@app.route('/translate', methods=['POST'])
def trans():
    message = request.form['message']

    tr = paraphrase.paraphrase()
    trans = tr.manyResult(message) # paraphrase

    if len(trans) > 7:
        transL = 7
    else:
        transL = len(trans)
    
    response = ""

    for i in range(0,transL):

        response += """
            <div class="chat-bubble result">
                <span class="chat-content order{1}" onclick='speakPara({1})' title="듣기">
                    {0}
                </span>
                <img class="insert" src="/static/insert.png" onclick='goPara({1})'/>
            </div>
        """.format(trans[i], i)

    response_text = {"message":  message, "result": response}

    return jsonify(response_text)

@app.route('/load', methods=['POST'])
def load():
    time = request.form['time']
    userid = session['userid']

    uM = user.memberManage()
    paragraph = uM.lookPara(userid, time)

    return paragraph

@app.route('/speak', methods=['POST'])
def speak():
    message = request.form['message']

    tts = gTTS(text=message, lang='en')
    filename = 'tmp/speak.mp3'
    tts.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    music.play()

    sleep(music.duration) #prevent from killing
    os.remove(filename) #remove temperory file

    return 'speak'

@app.route('/insert', methods=['POST'])
def insert():
    message = request.form['message']

    message = message.replace("'", "''")

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

    if 'logged_in' in session and session['logged_in']: # login한 사용자는 저장.
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

@app.route('/save', methods=['POST'])
def save():
    text = request.form['text']

    if 'logged_in' in session and session['logged_in']:
        mM = user.memberManage()

        mM.insertPara(session['userid'], text)

        return jsonify({"message": "저장되었습니다."})
    else:
        return jsonify({"message": "로그인한 사용자만 이용 가능합니다."})
  

# run Flask app
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()