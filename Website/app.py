from flask import Flask, render_template, url_for, request

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
# from app import mail

# from flask.Flask import Flask from flaskext.mail import Mail, Message

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

msg = Message('Halo aku mau tes email dlu yah', recipients=['fahira1678@gmail.com'])
msg.body = 'This is a test email!'
msg.html = '<p>This is a test email!</p>'

mail.send(msg)

@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('user.html')

@app.route("/diagnosa", methods=['GET', 'POST'])
def diagnosa():

    usia = request.form['usia']
    return render_template('diagnosa.html', usia=usia)

@app.route("/history")
def history():
    return render_template('history.html')

app.run(debug=True)   

