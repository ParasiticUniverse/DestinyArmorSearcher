import os
import sys
import uuid
from flask import Flask, request, render_template, redirect
import requests
import json

app = Flask(__name__)

BASE_URL="https://www.bungie.net/"
URL_AUTH=f"{BASE_URL}en/oauth/authorize"
URL_TOK=f"{BASE_URL}Platform/app/oauth/token/"

AUTH_TOK=None
API_KEY=None
CLIENT_ID=None
STATE=None

def obtain_authToken(code):

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'client_id': CLIENT_ID}

    try:
        r = requests.post(URL_TOK, headers=headers, data=data)
    except requests.ConnectionError as err:
        return None


    return r.json()['access_token']


@app.route('/callback')
def bungie_callback():

    stateResponse = request.args.get('state')
    
    if stateResponse == STATE:
        code = request.args.get('code')
        AUTH_TOK = obtain_authToken(str(code))

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def home():

    url = f"{URL_AUTH}?client_id={CLIENT_ID}&response_type=code&state={STATE}"

    return render_template('index.html', url_auth=url)


if __name__=='__main__':

    API_KEY = os.getenv('API_KEY', None)
    CLIENT_ID = os.getenv('CLIENT_ID', None)
    STATE = uuid.uuid4().hex

    if API_KEY is None or CLIENT_ID is None:
        sys.exit('Environment variable not set up for API_KEY/CLIENT_ID')

    app.run(ssl_context='adhoc')
