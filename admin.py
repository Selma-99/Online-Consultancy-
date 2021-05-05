from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route("/admin_home")
def admin_home():
	return render_template("admin_home.html")

@admin.route("/admin_manage_doctor",methods=['get','post'])
def admin_manage_doctor():
	data={}
	q="SELECT * FROM `hospitals`"
	data['hospital']=select(q)
	q="SELECT * FROM `hospitals` inner join doctors using(hospital_id)"
	data['doctor_view']=select(q)
	if 'action' in request.args:
		action=request.args['action']
		did=request.args['did']

	else:
		action=None
	if action=='delete':
		q="delete from doctors where login_id='%s'"%(did)
		delete(q)
		q="delete from login where login_id="'%s'%(did)
		delete(q)
		return redirect(url_for('admin.admin_manage_doctor'))
	if action=='update':
		q="select * from doctors inner join hospitals using(hospital_id) where login_id='%s'"%(did)
		data['updatess']=select(q)

	if 'submits' in request.form:
		hosp=request.form['hosp']
		dept=request.form['dept']
		dname=request.form['dname']
		phone=request.form['phone']
		email=request.form['email']
		
		q="update `doctors` set `hospital_id`='%s',`dept`='%s',`dname`='%s',`phone`='%s',`email`='%s' where login_id='%s'"%(hosp,dept,dname,phone,email,did)
		update(q)
		return redirect(url_for("admin.admin_manage_doctor"))
	if 'submit' in request.form:
		hosp=request.form['hosp']
		dept=request.form['dept']
		dname=request.form['dname']
		phone=request.form['phone']
		email=request.form['email']
		q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('%s','%s','doctor')"%(email,phone)
		lid=insert(q)
		q="INSERT INTO `doctors`(`login_id`,`hospital_id`,`dept`,`dname`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s','%s')"%(lid,hosp,dept,dname,phone,email)
		insert(q)
		return redirect(url_for("admin.admin_manage_doctor"))

	return render_template("admin_manage_doctor.html",data=data)	

@admin.route("/admin_manage_hospital",methods=['get','post'])
def admin_manage_hospital():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		hid=request.args['hid']

	else:
		action=None
	if action=='delete':
		q="delete from hospitals where hospital_id='%s'"%(hid)
		delete(q)
		
		return redirect(url_for('admin.admin_manage_hospital'))

	if action=='update':
		q="select * from hospitals where hospital_id='%s'"%(hid)
		data['updatess']=select(q)
		if 'submits' in request.form:

			hospital=request.form['hospital']
			place=request.form['place']
			phone=request.form['phone']
			q="update `hospitals` set `hospital`='%s',`place`='%s',`phone`='%s' where hospital_id='%s'"%(hospital,place,phone,hid)
			update(q)
			return redirect(url_for("admin.admin_manage_hospital"))



	data['selma']=2
	q="SELECT * FROM hospitals"
	data['hospital']=select(q)
	if 'submit' in request.form:
		hname=request.form['hname']
		place=request.form['place']
		phone=request.form['phone']

		q="INSERT INTO `hospitals`(`hospital`,`place`,`phone`) VALUES('%s','%s','%s')"%(hname,place,phone)
		insert(q)
		return redirect(url_for("admin.admin_manage_hospital"))

	return render_template("admin_manage_hospital.html",data=data)	

@admin.route("/admin_view_patient")
def admin_view_patient():
	data={}
	q="SELECT * FROM `patient`"
	data['patient']=select(q)
	return render_template("admin_view_patient.html",data=data)	

@admin.route("/admin_view_patient_precaution")
def admin_view_patient_precaution():
	data={}
	q="SELECT * FROM `precaution`"
	data['precaution']=select(q)
	return render_template("admin_view_patient_precaution.html",data=data)	

	

@admin.route("/admin_filesuploaded")
def admin_filesuploaded():
	return render_template("admin_filesuploaded.html")	