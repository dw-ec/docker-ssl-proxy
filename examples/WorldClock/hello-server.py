from flask import Flask, request
from flask_restful import Resource, Api
import requests, json

app = Flask(__name__)

@app.route('/time/<continent>/<city>')
def hello_time(continent=None, city=None):

    try:
        time = requests.get("https://{}.clock.demo/{}".format(continent, city)).content.decode("utf-8")
        return 'Hello World! The time sponsored by https://{}.clock.demo/ is: {}'.format( continent, time )
    except:
        return "Hello World! I don't know what the time is in {}/{}".format(
                continent, city)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run('0.0.0.0','80')
