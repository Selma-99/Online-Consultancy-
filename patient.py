from flask import *
from database import *
import uuid


import os
from flask import Flask, jsonify

from flask.globals import request, session
from werkzeug.utils import secure_filename

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

patient=Blueprint('patient',__name__)

@patient.route('/patient_home')
def patient_home():
	if not session.get("lid") is None:
		
		return render_template("patient_home.html")
	else:
		return redirect(url_for("public.login"))

@patient.route('/patient_view_hospital')
def patient_view_hospital():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `hospitals`"
		data['hospital']=select(q)
		return render_template("patient_view_hospital.html",data=data)
	else:
		return redirect(url_for("public.login"))



@patient.route('/patient_view_doctor')
def patient_view_doctor():
	if not session.get("lid") is None:
		data={}
		hid=request.args['hid']
		q="SELECT * FROM `doctors` where hospital_id='%s'"%(hid)
		data['doctor']=select(q)
		return render_template("patient_view_doctor.html",data=data)
	else:
		return redirect(url_for("public.login"))


@patient.route('/patient_chat_with_doctor',methods=['get','post'])
def patient_chat_with_doctor():
	if not session.get("lid") is None:
		data={}
		
		pid=session['pid']
		did=request.args['did']
		q="SELECT * FROM `chats` WHERE (`sender_id`='%s' AND `reciever_id`='%s' AND `sender_type`='patient') OR (`sender_id`='%s' AND `reciever_id`='%s' AND `sender_type`='doctor')"%(pid,did,did,pid)
		data['chat']=select(q)
		if 'submit' in request.form:
			message=request.form['message']
			q="INSERT INTO `chats`(`sender_id`,`reciever_id`,`sender_type`,`message`,`date_time`) VALUES('%s','%s','patient','%s',now())"%(pid,did,message)
			insert(q)
			return redirect(url_for('patient.patient_chat_with_doctor',did=did))
		return render_template("patient_chat_with_doctor.html",data=data)
	else:
		return redirect(url_for("public.login"))


@patient.route('/patient_upload_illness',methods=['get','post'])
def patient_upload_illness():
	if not session.get("lid") is None:
		data={}
		did=request.args['did']
		data['did']=did
		q="SELECT * FROM `files` INNER JOIN `doctors` USING(doctor_id) where patient_id='%s' and doctor_id='%s'"%(session['pid'],did)
		data['ill']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from `files` where file_id='%s'"%(id)
			delete(q)
			flash('Deleted...')
			return redirect(url_for('patient.patient_upload_illness',did=did))

		if 'submit' in request.form:
			ill=request.form['ill']
			sym=request.form['sym']
			file=request.files['file']
			path="static/"+str(uuid.uuid4())+file.filename
			file.save(path)
			q="INSERT INTO `files` (`patient_id`,`doctor_id`,`uploadfile`,`illness`,`symptoms`,`date`) VALUES('%s','%s','%s','%s','%s',curdate())"%(session['pid'],did,path,ill,sym)
			insert(q)
			flash('Uploaded Successfully...')
			return redirect(url_for('patient.patient_upload_illness',did=did))
		return render_template("patient_upload_illness.html",data=data)
	else:
		return redirect(url_for("public.login"))


@patient.route('/patient_view_precaution')
def patient_view_precaution():
	if not session.get("lid") is None:
		data={}
		fid=request.args['fid']
		q="SELECT * FROM `files` INNER JOIN `doctors` USING(`doctor_id`) INNER JOIN `precaution` USING(`file_id`) WHERE `file_id`='%s'"%(fid)
		data['precaution']=select(q)
		return render_template("patient_view_precaution.html",data=data)
	else:
		return redirect(url_for("public.login"))


@patient.route('/patient_add_rating',methods=['get','post'])
def patient_add_rating():
	if not session.get("lid") is None:
		if 'submit' in request.form:
			rate=request.form['rate']
			q="INSERT INTO `rate`(`user_id`,`rated`,`date`) VALUES('%s','%s',curdate())"%(session['pid'],rate)
			insert(q)
			flash('success...')
		
		return render_template("patient_add_rating.html")
	else:
		return redirect(url_for("public.login"))









@patient.route('/send_notification',methods=['get','post'])
def send_notification():
	if not session.get("lid") is None:
		data={}
		q="select * from doctors"
		res=select(q)
		data['doctors']=res
		q="select * from notification inner join doctors using(doctor_id) where patient_id='%s'"%(session['pid'])
		res=select(q)
		data['not']=res
		print(data['not'],'..................')		
		if 'submit' in request.form:
			doctor_id=request.form['doctor_id']
			notification=request.form['notification']
			q="insert into notification values(NULL,'%s','%s','%s',now(),'pending')"%(session['pid'],doctor_id,notification)
			insert(q)


			q="select * from doctors where doctor_id='%s'"%(doctor_id)
			res4=select(q)
			e_mail=str(res4[0]['email'])
			q="select * from patient where patient_id='%s'"%(session['pid'])
			res5=select(q)
			username=str(res5[0]['fname'])+str(res5[0]['lname'])
			phone=str(res5[0]['phone'])
			try:
				gmail = smtplib.SMTP('smtp.gmail.com', 587)

				gmail.ehlo()

				gmail.starttls()

				gmail.login('zoyanv123@gmail.com','projectmca')

			except Exception as e:
				print("Couldn't setup email!!"+str(e))

			msg = MIMEText("sender name :" + username +" and notification  :" + notification+"  phone:"+phone  )
			# msg = MIMEText("Your password is Haii")

			msg['Subject'] = 'Notification From Patient'

			msg['To'] = e_mail

			msg['From'] = 'zoyanv123@gmail.com'

			try:

				gmail.send_message(msg)
				print(msg)
				print(e_mail)

			except Exception as e:

				print("COULDN'T SEND EMAIL", str(e))









			return redirect(url_for('patient.send_notification'))


		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from notification where notification_id='%s'"%(id)
			delete(q)
			flash('Deleted...')
			return redirect(url_for('patient.send_notification'))
			
		
		return render_template("patient_send_notification.html",data=data)
	else:
		return redirect(url_for("public.login"))