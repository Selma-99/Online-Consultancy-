from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def main_home():
	session.clear()
	
	return render_template("main_home.html")




@public.route('/login',methods=['get','post'])
def login():
	session.clear()


	if 'submit' in request.form:
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="select * from login where username='%s' and password='%s'"%(uname,pwd)
		res=select(q)

		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.admin_home'))
			
			elif res[0]['usertype']=='doctor':
				q1="select * from doctors where login_id='%s'"%(session['lid'])
				res1=select(q1)
				if res1:

					session['did']=res1[0]['doctor_id']
					q="select * from doctors where doctor_id='%s'"%(session['did'])
					res=select(q)
					session['d_name']=res[0]['doctor_name']
					return redirect(url_for('doctor.doctor_home'))
			elif res[0]['usertype']=='patient':
				q1="SELECT *,CONCAT(`fname`,' ',`lname`)AS `name` FROM patient WHERE login_id='%s'"%(session['lid'])
				res1=select(q1)
				if res1:

					session['pid']=res1[0]['patient_id']
					session['p_name']=res1[0]['name']
					
					return redirect(url_for('patient.patient_home'))
		else:
			flash('Access Denied...Register To Login')

			
	
		

	return render_template('login.html')


@public.route('/patient_register',methods=['get','post'])
def patient_register():
	session.clear()
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phone=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('%s','%s','patient')"%(uname,pwd)
		lid=insert(q)
		q="INSERT INTO `patient` (`login_id`,`fname`,`lname`,`phone`,`email`) VALUES('%s','%s','%s','%s','%s')"%(lid,fname,lname,phone,email)
		insert(q)
		flash('Registered Successfully...')
		return redirect(url_for('public.login'))
	
	return render_template("patient_register.html")