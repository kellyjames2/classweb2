from flask import Flask, render_template, request, flash, Blueprint
from flask_login import login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import UserMixin
import uuid
import time

db = SQLAlchemy()
DB_NAME = "database.db"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    indnum = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(150))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_PERMANENT"] = False
    db.init_app(app)

    from main import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('flasktutorials/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

from main import create_app
from main import User

app = create_app()

import uuid
from main import User, db
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, send_from_directory, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

list = [
                        "UED2901924", "UED2901724", "UED2901324", "UED2901024", "UED2900924",
                        "UED2901224", "UED2901824", "UED2900624", "UED2900224", "UED2901442",
                        "UED2900824", "UED2902424", "UED2901524", "UED2503924", "UED2900324",
                        "UED2900124", "UED2902024", "UED2902724", "UED2901624", "UED2900524",
                        "UED2900424", "UED2901124", "UED2900724", "UED2902624", "UED2507224",
                        "UED2902724", "UED2902324", "UED2902824", "UED2902224", "UED2902524",
                        "UED2902124"
        ]
students = [
    "Joseph", "Ehud", "Edwin", "Douglas", "Vincent",
    "Michael", "Esther", "Cecilia", "Rocklyn", "Anthoinette",
    "Chris", "Asantewaa", "Zeinab", "Comfort", "Pregitta",
    "Asante", "Evelyn", "David", "Kelvin", "Boakye",
    "Solomon", "Ernest", "Patrick", "Bernard", "Kinsley",
    "David", "Najat", "Daniel", "Caleb", "Nyame-Do"
    "Gmayun", "Alexis"
    ]
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    from main import app
    if request.method == 'POST':
        indnum = request.form.get('indnum')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(indnum=indnum).first()
        if indnum in list:
            if user:
                flash('Index Number already exists.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                new_user = User(indnum=indnum, password=generate_password_hash(password1, method='scrypt'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=False)
                flash('Account created!', category='success')
                return redirect(url_for('home'))
        else:
            flash("Index Number is not supported!", category="error")

    return render_template("signup.html", user=current_user)


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    from datetime import datetime
    from main import list, students
    courses = [
        ("Principles Of Programming", "this is pop"),
        ("Computer Packages", "this is comp pack"),
        ("Information Systems", "this is is"),
        ("Computer Ethics", "this is ethics"),
        ("Fundamentals Of Computing", "this is foc"),
        ("French", "this is french"),
        ("Academic Writing", "this is aw"),
        ("Calculus", "this is calculus")
    ]
    now = datetime.now()
    current_hour = now.hour
    if 0 <= current_hour <= 11:
        greeting = "Good Morning"
    elif 11 < current_hour <= 15:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    name = list.index(current_user.indnum)
    student_name = students[name]
    folder_path = "static/recentup"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("home.html", student_name=student_name, user=current_user, greeting=greeting, courses=courses, files=files)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        indnum = request.form.get("indnum")
        password = request.form.get("password")
        
        user = User.query.filter_by(indnum=indnum).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in successfully", category="success")
                login_user(user, remember=False)
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password", category="error")
        else:
            flash("Index number is not supported", category="error")
        
    return render_template('login.html', user=current_user)

"""@app.before_request
def check_session_token():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if not user or user.session_token != session.get("session_token"):
            session.clear()
            return redirect(url_for("login"))"""

@app.route("/slides")
@login_required
def slidespage():
    """courses = [
        "Principles Of Programming",
        "Computer Packages",
        "Information Systems",
        "Computer Ethics",
        "Fundamentals Of Computing",
        "French",
        "Academic Writing",
        "Calculus"
    ]
    value = [
        "pop",
        "cp",
        "is",
        "ce",
        "foc",
        "french",
        "aw",
        "calculus"
    ]//"""
    return render_template("slidespage.html")

@app.route("/download/<pathoffolder>/<filename>")
def download_file(filename, pathoffolder):
    path = f"static/{pathoffolder}"
    return send_from_directory(path, filename, as_attachment=True)

@app.route("/view/<pathoffolder>/<filename>")
def view_file(filename, pathoffolder):
    path = f"static/{pathoffolder}"
    return send_from_directory(path, filename, as_attachment=False)


@app.route("/pop")
def pop():
    folder_path = "static/pop"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("pop.html", topics=topics)

@app.route("/cp")
def cp():
    folder_path = "static/cp"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("cp.html", topics=topics)

@app.route("/iss")
def iss():
    folder_path = "static/iss"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("iss.html", topics=topics)

@app.route("/ce")
def ce():
    folder_path = "static/ce"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("ce.html", topics=topics)

@app.route("/foc")
def foc():
    folder_path = "static/foc"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("foc.html", topics=topics)

@app.route("/french")
def french():
    folder_path = "static/french"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("french.html", topics=topics)

@app.route("/aw")
def aw():
    folder_path = "static/aw"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("aw.html", topics=topics)

@app.route("/calculus")
def calculus():
    folder_path = "static/calculus"
    topics = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return render_template("calculus.html", topics=topics)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)), host='0.0.0.0')