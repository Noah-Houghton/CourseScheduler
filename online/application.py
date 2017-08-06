# Implements a backend for a website allowing users to submit, search, and manage posts with administrative functionality for specific users

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import time
from helpers import *
from datetime import datetime, timedelta
from flask_jsglue import JSGlue

# configure application
app = Flask(__name__)
jsglue = JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET"])
def root():
    """Redirect a user to the homepage"""
    if request.method == "GET":
        # direct user to home page
        return redirect(url_for("home"))

@app.route("/home", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        """Home page, displays current courseload and requirements"""
        # for pre-user implementation debugging
        session["user_id"] = 1
        # end debug script
        crses = activeCourses(session["user_id"])
        COS = activeCOS(session["user_id"])
        return render_template("home.html", crs_data = crses, COS_data = COS)

@app.route("/search", methods = ["GET", "POST"])
def search():
    return render_template("search.html")

# extracts entries based on user's entry
@app.route("/doSearch", methods=["GET"])
@login_required
def doSearch():
    """Process request from search.js and jsonify it"""
    if request.method == "GET":
        # seeks query entry from HTML
        q = request.args.get("q")
        # figure out which types should be included in search
        types = request.args.get("types")
        rows = search(q, types)
        cutoff = 200
        # returns object
        return jsonify(rows[:cutoff])

@app.route("/account", methods = ["GET", "POST"])
def account():
    return render_template("account.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        db = sqlite3.connect("users.db")
        usr = request.form.get("username")
        print(usr)
        pswd = request.form.get("password")
        print(pswd)
        pswd_hash = pwd_context.encrypt(pswd)
        try:
            db.execute("INSERT INTO Users (username, password) Values (?, ?)", (usr, pswd_hash))
            db.commit()
            db.close()
            return redirect(url_for("home"))
        except:
            return apology("Could not register user. Please contact support.")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        db = sqlite3.connect("users.db")
        session.clear()
        # look up account in database
        # get entered information from HTML form
        name = request.form.get("username")
        rows = db.execute("SELECT * FROM Users WHERE username=?", (name,))
        print(name)
        try:
            passw = request.form.get("password")
            print(passw)
            if not pwd_context.verify(passw, rows[0]["password"]):
                raise Exception
            session[user_id] = rows[0]["ID"]
            session[user_type] = rows[0]["usr_type"]
            # user is logged in, return them to home page
            return redirect(url_for("home"))
        except:
            return apology("invalid username or password")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    return render_template("logout.html")