from flask import *
from database import *
import uuid

doctor=Blueprint('doctor',__name__)

@doctor.route('/doctor_home')
def doctor_home():
	if not session.get("lid") is None:
		return render_template("doctor_home.html")
	else:
		return redirect(url_for("public.login"))

@doctor.route('/doctor_view_profiles',methods=['get','post'])
def doctor_view_profiles():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`fname`,' ',`lname`)AS `name` FROM `patient`"
		data['profile'] =select(q)

		if 'action' in request.args:
			action=request.args['action']
			data['action']=action
			pid=request.args['pid']
			data['pid']=pid
		else:
			action=None
		if action=='view':


			q="SELECT *,CONCAT(`fname`,' ',`lname`)AS `name` FROM `patient`    WHERE  `patient_id`='%s'"%(pid)
			res=select(q)
			data['patient']=res
			data['name']=res[0]['name']
			data['phone']=res[0]['phone']
			data['email']=res[0]['email']
		if action=='illness':
			q="SELECT *,CONCAT(`fname`,' ',`lname`)AS `name` FROM `patient`  INNER JOIN `files` USING(`patient_id`)  WHERE `doctor_id`='%s' and  `patient_id`='%s'"%(session['did'],pid)
			res=select(q)
			if res:
				data['illness']=res
				data['name']=res[0]['name']
				data['phone']=res[0]['phone']
				data['email']=res[0]['email']
				data['ill']=res[0]['illness']
				data['symptoms']=res[0]['symptoms']
				data['file']=res[0]['uploadfile']
				data['date']=res[0]['date']
			else:
				flash('No Data Found!!')
				return redirect(url_for('doctor.doctor_view_profiles'))
		# if action=='precaution':
		# 	q="SELECT *,CONCAT(`fname`,' ',`lname`)AS `name` FROM `patient`  INNER JOIN `files` USING(`patient_id`)  WHERE `doctor_id`='%s' and  `patient_id`='%s'"%(session['did'],pid)
		# 	res=select(q)
		# 	file_id=res[0]['file_id']
		# 	q1=""
		# 	data['patient']=res
		# 	data['name']=res[0]['name']
		# 	data['phone']=res[0]['phone']
		# 	data['email']=res[0]['email']

		return render_template("doctor_view_profiles.html",data=data)
	else:
		return redirect(url_for("public.login"))


@doctor.route('/doctor_upload_precaution',methods=['get','post'])
def doctor_upload_precaution():
	if not session.get("lid") is None:
		data={}
		pid=request.args['pid']
		fid=request.args['fid']
		q="SELECT * FROM `precaution` INNER JOIN `files` USING(`file_id`) WHERE `patient_id`='%s'"%(pid)
		data['precaution']=select(q)

		if 'submit' in request.form:
			pre=request.form['pre']
			file=request.files['file']
			path="static/"+str(uuid.uuid4())+file.filename
			file.save(path)
			q="INSERT INTO `precaution` (`file_id`,`details`,`filepath`,`date`) VALUES('%s','%s','%s',curdate())"%(fid,pre,path)
			insert(q)
			flash('success...')
			return redirect(url_for('doctor.doctor_upload_precaution',pid=pid,fid=fid))
		return render_template("doctor_upload_precaution.html",data=data)
	else:
		return redirect(url_for("public.login"))

@doctor.route('/doctor_chat',methods=['get','post'])
def doctor_chat():
	if not session.get("lid") is None:
		data={}
		
		pid=request.args['pid']
		did=session['did']
		q="SELECT * FROM `chats` WHERE (`sender_id`='%s' AND `reciever_id`='%s' AND `sender_type`='doctor') OR (`sender_id`='%s' AND `reciever_id`='%s' AND `sender_type`='patient')"%(did,pid,pid,did)
		data['chat']=select(q)
		if 'submit' in request.form:
			message=request.form['message']
			q="INSERT INTO `chats`(`sender_id`,`reciever_id`,`sender_type`,`message`,`date_time`) VALUES('%s','%s','doctor','%s',now())"%(did,pid,message)
			insert(q)
			return redirect(url_for('doctor.doctor_chat',pid=pid))
		return render_template("doctor_chat.html",data=data)
	else:
		return redirect(url_for("public.login"))


@doctor.route('/doctor_view_rating')
def doctor_view_rating():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `rate` INNER JOIN `patient` ON(`patient`.`patient_id`=`rate`.`user_id`)"
		data['rating']=select(q)
		return render_template("doctor_view_rating.html",data=data)
	else:
		return redirect(url_for("public.login"))