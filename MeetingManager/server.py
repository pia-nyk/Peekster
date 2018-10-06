import os
from flask import Flask,jsonify,request,render_template,Response,redirect
from flaskext.mysql import MySQL
import hashlib
from flask import session
from werkzeug.utils import secure_filename
from test import convert 
from nltktrial import summarize
import time

UPLOAD_FOLDER = '/home/sunaina/Meeting_Manager/MeetingManager/static/assets/uploads'
ALLOWED_EXTENSIONS = set(['wav','mp3'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'Sunaina'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Stanley!1197'
app.config['MYSQL_DATABASE_DB'] = 'Meeting_Manager'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

	
conn = mysql.connect()
cursor=conn.cursor()

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/signup", methods=['GET','POST'])
def signup():
	name = request.form["name"]
	username = request.form["username"]
	password = request.form["pass1"]
	email = request.form["email"]
	
	cursor.execute("SELECT user_name From USER WHERE user_name = '"+username+"';")
	result = cursor.fetchone()
	if(result is not None):
		return render_template('signup.html')
	hash_object_password = hashlib.md5(password.encode())
	print(password)
	print(hash_object_password.hexdigest())
	password = hash_object_password.hexdigest()
	cursor.execute("INSERT INTO `USER` (`user_name`, `password`, `email_id`) VALUES ('"+username+"', '"+password+"', '"+email+"');")
	conn.commit()
	return render_template("login.html")

@app.route("/loginpage", methods=['GET','POST'])
def login_page():
	return render_template('login.html')


@app.route("/login",methods=['GET','POST'])
def login():
	username = request.form["username"]
	password = request.form["pass1"]
	hash_object_password = hashlib.md5(password.encode())
	password = hash_object_password.hexdigest()
	cursor.execute("SELECT `password` FROM `USER` WHERE user_name='"+username+"' ;")
	result = cursor.fetchone()
	if(result is None):
		return render_template("login.html")
	if(result[0]==password):
		session['username'] = username
		return render_template('profile.html',username=username)
	else:
		return render_template("login.html")

@app.route("/profile_page")
def profile_page():
	return render_template('profile.html', username=session['username'])

@app.route("/record_page")
def record_page():
	return render_template('record.html', username=session['username'])

@app.route("/upload_page")
def upload_page():
	return render_template('upload.html', username=session['username'])

@app.route("/upload",methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		#time.sleep(3)
		filename_full = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		meeting_name = request.form["meeting_name"]
		transcript, onlytext = convert(filename_full)
		summarizedText = summarize(onlytext)
		file_name = filename[0:-4]+"_t.txt"
		sum_file_name = filename[0:-4]+"_s.txt"
		with open(file_name, "w") as text_file:
			text_file.write(transcript)
		with open(sum_file_name,"w") as text_file:
			text_file.write(summarizedText)
		#print type(transcript)
		#print transcript 		
		#transcript = "abcde"
		cursor.execute("INSERT INTO `MEETING` (`meeting_name`, `summary`, `transcript`) VALUES ('"+meeting_name+"', '"+file_name+"', '"+sum_file_name+"');")
		conn.commit()
		print filename
	return render_template('upload.html', username=session['username'])

@app.route("/search_page")
def search_page():
	return render_template('search.html', username=session['username'])

@app.route("/searchdata",methods=['GET','POST'])
def search_results():
	meeting_name = request.form["textbox"]
	cursor.execute("select summary,transcript from MEETING where meeting_name='"+meeting_name+"';")
	result = cursor.fetchall()
	filename = result[0][0].encode("utf-8")
	openfile = result[0][1].encode("utf-8")
	with open(filename) as fp:
		lines1 = fp.read()
	with open(openfile) as fp:
		lines2 = fp.read()
	return render_template('search.html',transcript=lines1,summary=lines2)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5050, debug=True,threaded=True)



