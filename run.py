from flask import Flask, request, jsonify, render_template
import os
import requests
import json
import pusher
import httplib2
import json
import urllib.request
from konlpy.tag import Okt
from collections import Counter
import pymysql
from datetime import datetime

h = httplib2.Http()
okt = Okt()

app = Flask(__name__)

channels_client = pusher.Pusher(
  app_id='785530',
  key='17e9426b449b62f3005a',
  secret='82a343a878619f1936c4',
  cluster='ap3',
  ssl=True
)

@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run()