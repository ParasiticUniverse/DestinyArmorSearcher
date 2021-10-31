import os
from flask import Flask, request, render_template, redirect
import requests
import json

app = Flask(__name__)

BASE_URL="https://www.bungie.net/"
URL_AUTH=f"{BASE_URL}en/oauth/authorize"
URL_TOK=f"{BASE_URL}Platform/app/oauth/token/"
STATE=''

AUTH_TOK = None
API_KEY=''
CLIENT_ID=''

def obtain_authToken(code):

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'client_id': CLIENT_ID}

    try:
        r = requests.post(URL_TOK, headers=headers, data=data)
    except requests.ConnectionError as err:
        print(err.message)
        return None


    return r.json()['access_token']


@app.route('/callback')
def bungie_callback():

    state = request.args.get('state')
    code = request.args.get('code')
    AUTH_TOK = obtain_authToken(str(code))

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def home():

    url = f"{URL_AUTH}?client_id={CLIENT_ID}&response_type=code&state={STATE}"

    return render_template('index.html', url_auth=url)


if __name__=='__main__':
    API_KEY = os.getenv('API_KEY')
    CLIENT_ID = os.getenv('CLIENT_ID')

    app.run(ssl_context='adhoc')
