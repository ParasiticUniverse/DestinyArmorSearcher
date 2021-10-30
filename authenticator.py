from flask import Flask, request, render_template, url_for, redirect
import requests

app = Flask(__name__)

URL_AUTH="https://www.bungie.net/en/oauth/authorize"
URL_TOK="https://www.bungie.net/Platform/app/oauth/token/"
API_KEY=""

CLIENT_ID=""
STATE = ""

def obtain_authToken(code):
    
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'client_id': CLIENT_ID} 

    r = requests.post(f"{URL_TOK}", headers=HEADERS, data=data)

    print(r.json())


@app.route('/callback')
def bungie_callback():

    state = request.args.get('state')
    code = request.args.get('code')
    obtain_authToken(str(code))

    return redirect('/')

# set up:
# export FLASK_APP=authenticator
# export FLASK_ENV=development
# flask run --cert=adhoc
@app.route('/', methods=['GET', 'POST'])
def home():
    url = f"{URL_AUTH}?client_id={CLIENT_ID}&response_type=code&state={STATE}"

    return render_template('index.html', url_auth=url)

