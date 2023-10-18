from flask import Flask, render_template, request, redirect, url_for, flash, session,g
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField , BooleanField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from pymongo import MongoClient
from flask_caching import Cache
import time
from bson import ObjectId
import os
from dotenv import load_dotenv
import pymongo
import logging
from functools import wraps 

load_dotenv()

app = Flask(__name__)
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo_uri = os.environ.get('MONGO_URI')
sqlite_db_path = os.environ.get('SQLITE_DB_PATH','myusers.db')

client = MongoClient(mongo_uri)
db = client["?"]
collection = db["?"]
applications_collection = db['?']


cache = Cache(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# SQLite database setup
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()


cursor.execute('''
   CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY,
       username TEXT NOT NULL,
       password TEXT NOT NULL,
       role TEXT NOT NULL    
   )
''')
conn.commit()
conn.close()



job1 = {
    "url" : "../static/tech.png",
    "job_title": "Software Engineer",
    "company_name": "TechCo Inc.",
    "location": "San Francisco, CA",
    "job_description": "We are looking for a skilled software engineer to join our team...",
    "application_instructions": "Please apply here and we will contact you to get the CV and more informations.",
    "price_range": "$80,000 - $120,000",
    "duration": "Full-time",
    "requirements": {
        "education": "Master's degree in Computer Science or related field",
        "experience": "2+ years of software development experience"
    }
}

job2 = {
    "url" : "../static/data.jpeg",
    "job_title": "Data Analyst",
    "company_name": "Data Analytics Corp.",
    "location": "New York, NY",
    "job_description": "We are seeking a data analyst to work on data-driven projects...",
    "application_instructions": "Please apply here and we will contact you to get the CV and more informations.",
    "price_range": "$60,000 - $90,000",
    "duration": "Full-time",
    "requirements": {
        "education": "Bachelor's or Master's degree in Data Science, Statistics, or related field",
        "experience": "1+ year of data analysis experience"
    }
}

job3 = {
    "url" : "../static/go.png",
    "job_title": "Web Developer",
    "company_name": "Google",
    "location": "Los Angeles, CA",
    "job_description": "We need a talented web developer to build and maintain our websites...",
    "application_instructions": "Please apply here and we will contact you to get the CV and more informations.",
    "price_range": "$70,000 - $110,000",
    "duration": "Full-time",
    "requirements": {
        "education": "Bachelor's or Master's degree in Computer Science or related field",
        "experience": "2+ years of web development experience"
    }
}

job4 = {
    "url" : "../static/net.jpeg",
    "job_title": "Network Administrator",
    "company_name": "NetSys Inc.",
    "location": "Chicago, IL",
    "job_description": "Join our IT team as a network administrator and manage our network infrastructure...",
    "application_instructions": "Please apply here and we will contact you to get the CV and more informations.",
    "price_range": "$60,000 - $100,000",
    "duration": "Full-time",
    "requirements": {
        "education": "Bachelor's or Master's degree in IT, Networking, or a related field",
        "experience": "3+ years of network administration experience"
    }
}

job5 = {
    "url" : "../static/ai.jpeg",
    "job_title": "Machine Learning Engineer",
    "company_name": "AI Innovations LLC",
    "location": "Seattle, WA",
    "job_description": "Seeking a machine learning engineer to work on cutting-edge AI projects...",
    "application_instructions": "Please apply here and we will contact you to get the CV and more informations.",
    "price_range": "$90,000 - $140,000",
    "duration": "Full-time",
    "requirements": {
        "education": "Master's degree in Computer Science, Machine Learning, or related field",
        "experience": "2+ years of machine learning development experience"
    }
}


for job in [job1, job2, job3, job4, job5]:
    if collection.find_one({"job_title": job["job_title"]}) is None:
        collection.insert_one(job)


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('myusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user = User(user_data[0], user_data[1], user_data[3])
        return user
    return None



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=120)])
    admin = BooleanField('Register as Admin')
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=120)])
    submit = SubmitField('Log In')
    

@app.before_request
def before_request():
    g.request_start_time = time.time()

@app.after_request
def after_request(response):
    request_time = time.time() - g.request_start_time
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = sqlite3.connect('myusers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[3])
            login_user(user)

            if user_data[3] == 'admin':
                session['admin'] = True

            return redirect(url_for('home'))
        else:
            flash('Wrong password or username, please try again!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = 'admin' if form.admin.data else 'user'  # Assuming you have a checkbox in the registration form for admin selection

        conn = sqlite3.connect('myusers.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)
 



@app.route('/logout')
@login_required
def logout():
    session.pop('admin', None)
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
@login_required
def home():
    return render_template('home.html')



@app.route('/jobs')
def jobs():
    # Fetch all jobs from the MongoDB collection
    jobs = collection.find()
    
    return render_template('jobs.html', jobs=jobs)


@app.route('/job/<job_id>')
def job_detail(job_id):

    job = collection.find_one({"_id": ObjectId(job_id)})
    return render_template('job_detail.html', job=job)



@app.route('/job/<job_id>/submit_application', methods=['POST'])
@login_required  # To restrict access to authenticated users
def submit_application(job_id):
    if request.method == 'POST':
        app.logger.info(ObjectId(job_id))
        result = collection.find_one({'_id' : ObjectId(job_id)})
        app.logger.info(result)


        email = request.form['email']
        name = request.form['name']
        family_name = request.form['family_name']
        phone_number = request.form['phone_number']
        postal_code = request.form['postal_code']
        city = request.form['city']

        # Store the application data in MongoDB
        application_data = {
            'company_name' : result['company_name'],
            'job_title': result['job_title'],
            'user_id': current_user.id,
            'email': email,
            'name': name,
            'family_name': family_name,
            'phone_number': phone_number,
            'postal_code': postal_code,
            'city': city,
        }

  
        applications_collection.insert_one(application_data)

        flash('Application submitted successfully!', 'success')

        return redirect(url_for('jobs'))  

    return redirect(url_for('job_detail', job_id=job_id))

@app.route('/admin')
@login_required
def admin():
    if 'admin' in session and session['admin']:
        return render_template('admin.html')
    else:
        return render_template('error.html')
    

# Create a route for adding jobs, which is accessible only to admins
@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if 'admin' in session and session['admin']:
        if request.method == 'POST':
            # Extract job details from the form
            job_data = {
                "url": request.form.get('url'),
                "job_title": request.form.get('job_title'),
                "company_name": request.form.get('company_name'),
                "location": request.form.get('location'),
                "job_description": request.form.get('job_description'),
                "application_instructions": request.form.get('application_instructions'),
                "price_range": request.form.get('price_range'),
                "duration": request.form.get('duration'),
                "requirements": {
                    "education": request.form.get('requirements.education'),
                    "experience": request.form.get('requirements.experience')
                }

            }
            

            collection.insert_one(job_data)

            flash('Job added successfully!', 'success')
            return redirect(url_for('jobs'))  

        return render_template('admin.html')  
    else:
        flash('You do not have admin privileges to add jobs.', 'danger')
        return redirect(url_for('error.html'))  

if __name__ == '__main__':
    app.run(port=8080,debug=True)