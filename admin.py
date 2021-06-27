from flask import *
from database import *
import uuid

admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	if not session.get("lid") is None:
		return render_template("admin_home.html")
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_hospital',methods=['get','post'])
def admin_manage_hospital():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `hospitals`"
		data['hospital']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			hid=request.args['hid']
		else:
			action=None
		if action=='delete':
			q="delete from hospitals where hospital_id='%s'"%(hid)
			delete(q)
			flash('deleted...')
			return redirect(url_for('admin.admin_manage_hospital'))
		if action=='update':
			q="select * from hospitals where hospital_id='%s'"%(hid)
			print(q)
			data['updatess']=select(q)
		if 'submits' in request.form:
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			q="UPDATE `hospitals` SET `hospital`='%s',`place`='%s',`phone`='%s' where hospital_id='%s'"%(hname,place,phone,hid)
			update(q)
			flash('Updated Successfully...')
			return redirect(url_for('admin.admin_manage_hospital'))

		if 'submit' in request.form:
			hname=request.form['hname']
			place=request.form['place']
			phone=request.form['phone']
			q="INSERT INTO `hospitals`(`hospital`,`place`,`phone`) VALUES('%s','%s','%s')"%(hname,place,phone)
			insert(q)
			flash('Registered Successfully...')
			return redirect(url_for('admin.admin_manage_hospital'))
		return render_template("admin_manage_hospital.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_manage_doctor',methods=['get','post'])
def admin_manage_doctor():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,doctors.phone as dphone,doctors.email as demail FROM `doctors` INNER JOIN `hospitals` USING(`hospital_id`)"
		data['doctor']=select(q)
		q="select * from hospitals"
		data['hospital']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None
		if action=='delete':
			q="delete from doctors where doctor_id='%s'"%(did)
			delete(q)
			flash('deleted...')
			return redirect(url_for('admin.admin_manage_doctor'))
		if action=='update':
			q="SELECT * FROM `doctors` INNER JOIN `hospitals` USING(`hospital_id`) where doctor_id='%s'"%(did)
			print(q)
			data['updatess']=select(q)
		if 'submits' in request.form:
			hospiatl=request.form['hospiatl']
			dname=request.form['dname']
			phone=request.form['phone']
			email=request.form['email']

			q="UPDATE `doctors` SET `hospital_id`='%s',`doctor_name`='%s',`phone`='%s',`email`='%s' WHERE `doctor_id`='%s'"%(hospiatl,dname,phone,email,did)
			update(q)
			flash('Updated Successfully...')
			return redirect(url_for('admin.admin_manage_doctor'))

		if 'submit' in request.form:
			hospiatl=request.form['hospiatl']
			dname=request.form['dname']
			phone=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('%s','%s','doctor')"%(uname,pwd)
			lid=insert(q)
			q="INSERT INTO `doctors`(login_id,`hospital_id`,`doctor_name`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s')"%(lid,hospiatl,dname,phone,email)
			insert(q)
			flash('Registered Successfully...')
			return redirect(url_for('admin.admin_manage_doctor'))
		return render_template("admin_manage_doctor.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_view_patient',methods=['get','post'])
def admin_view_patient():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `patient`"
		data['patient']=select(q)
		

		return render_template("admin_view_patient.html",data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route('/admin_view_files',methods=['get','post'])
def admin_view_files():
	if not session.get("lid") is None:
		data={}
		pid=request.args['pid']
		q="SELECT *,`doctors`.`doctor_name` AS dname FROM `files` INNER JOIN `doctors` USING(`doctor_id`) INNER JOIN `precaution` USING(`file_id`) WHERE `patient_id`='%s'"%(pid)
		print(q)
		data['files']=select(q)
		

		return render_template("admin_view_files.html",data=data)
	else:
		return redirect(url_for("public.login"))


@admin.route('/admin_view_rating')
def admin_view_rating():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `rate` INNER JOIN `patient` ON(`patient`.`patient_id`=`rate`.`user_id`)"
		data['rating']=select(q)
		return render_template("admin_view_rating.html",data=data)
	else:
		return redirect(url_for("public.login"))
