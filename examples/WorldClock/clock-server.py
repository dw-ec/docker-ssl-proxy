from flask import Flask, request
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route('/<city>')
def time_in(city):

    try:
        hostname = request.headers.get( 
                'X-Forwarded-Host',
                request.headers['Host'])

        continent = hostname.split(".")[0]
        tz = pytz.timezone("{}/{}".format( continent, city ) )

    except:
        tz = pytz.timezone("UTC")

    cityTime = datetime.now(tz)
    return cityTime.strftime("\"{}: %H:%M:%S\"".format( tz.zone ))

@app.route('/')
def time():
    tz = pytz.timezone("UTC")
    return datetime.now(tz).strftime("\"UTC: %H:%M:%S\"")

if __name__ == '__main__':
    app.run('0.0.0.0','80')
