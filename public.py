from flask import *
from database import *

public=Blueprint('public',__name__)


@public.route('/')
def home():
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		uname=request.form['uname']
		psw=request.form['psw']
		q="SELECT * from login WHERE username='%s' AND password='%s'"%(uname,psw)
		res=select(q)
		if res:
			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.admin_home'))
			if res[0]['usertype']=='doctor':
				return redirect(url_for('doctor.doctor_home'))

		    # if res[0]['usertype']=='user':
		    	# return redirect(url_for('user.user_home'))

	return render_template('login.html')

@public.route('/register')
def register():
	return render_template('register.html')

@public.route("/view_rating")
def view_rating():
	return render_template("view_rating.html")