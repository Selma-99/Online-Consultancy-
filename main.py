from flask import *
from public import public
from admin import admin
from doctor import doctor
from patient import patient


import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail


app=Flask(__name__)
app.secret_key="asdfg"
app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(doctor,url_prefix='/doctor')
app.register_blueprint(patient,url_prefix='/patient')


mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'zoyanv123@gmail.com'
app.config['MAIL_PASSWORD'] = 'projectmca'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



		
app.run(debug=True,port=5012)