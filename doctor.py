from flask import *
from database import *

doctor=Blueprint('doctor',__name__)

@doctor.route("/doctor_home")
def doctor_home():
	return render_template("doctor_home.html")

@doctor.route("/doctor_view_details")
def doctor_view_details():
	data={}
	q="SELECT * FROM `patient`"
	data['patient']=select(q)
	return render_template("doctor_view_details.html",data=data)

@doctor.route("/doctor_view_uploadedfile")
def doctor_view_uploadedfile():
	return render_template("doctor_view_uploadedfile.html")


@doctor.route("/doctor_upload_precaution")
def doctor_upload_precaution():
	data={}
	q="SELECT * FROM `precaution`"
	data['precaution']=select(q)
	return render_template("doctor_upload_precaution.html",data=data)
	


	
	