from flask import *
from public import public
from admin import admin
from doctor import doctor


app=Flask(__name__)

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(doctor,url_prefix="/doctor")

app.run(debug=True)