from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Munchy"

def run():
  app.run(host='0.0.0.0',port=8080)

def pinger():
    t = Thread(target=run)
    t.start()