from flask import Flask, render_template, url_for, request

import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask('Ziramed App', static_url_path='/static')
# app = Flask("Google Login App")
app.secret_key = "ziramed.com"

# @app.route("/")
# def dashboard():
#     return render_template('index.html')

# @app.route("/login")
# def login():
#     return render_template('user.html')
import pickle
# # load the model from disk
filename = 'D:/Kuliah POLTEKPOS/Semester 5/Proyek TI III/Website/model_rf1.pkl'
loaded_model = pickle.load(open(filename, 'rb'))

@app.route("/diagnosa", methods=['GET', 'POST'])
def diagnosa():
    if request.method == 'GET':
        return render_template('diagnosa.html', name=session['name'])

    if request.method == 'POST':    
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        d = request.form['d']
        e = request.form['e']
        f = request.form['f']
        hasil = loaded_model.predict([[a, b, c, d, e, f]])

        return render_template('diagnosa.html', a=a, b=b, c=c, d=d, e=e, f=f, hasil=hasil)
    

@app.route("/history")
def history():
    return render_template('history.html')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "877419741968-knsqo3nrqqcgufcf1t9ldltlfg91i7du.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    print(session['name'])
    # return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    return redirect('/diagnosa')
    # return redirect(url_for('/diagnosa', , **request.args))


if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)   

