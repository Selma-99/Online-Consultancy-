import mysql.connector

username="root"
password=""
database="online_consultancy"
port=3306

def select(qry):
	con=mysql.connector.connect(user=username,password=password,host="localhost",database=database,port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(qry)
	result=cur.fetchall()
	cur.close()
	con.close()
	return result

def insert(qry):
	con=mysql.connector.connect(user=username,password=password,host="localhost",database=database,port=port)
	cur=con.cursor(dictionary=True)
	cur.execute(qry)
	con.commit()
	result=cur.lastrowid
	cur.close()
	con.close()
	return result

def update(q):
	cnx = mysql.connector.connect(user=username, password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result = cur.rowcount
	cur.close()
	cnx.close()
	return result

def delete(q):
	cnx = mysql.connector.connect(user=username, password=password, host="localhost", database=database,port=port)
	cur = cnx.cursor(dictionary=True)
	cur.execute(q)
	cnx.commit()
	result = cur.rowcount
	cur.close()
	cnx.close()