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

@app.route("/", methods = ["GET", "POST"])
# @login_required
def home():
    """Home page, displays current courseload and requirements"""
    # for pre-user debugging
    session["user_id"] = 1
    print(session["user_id"])
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
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    return render_template("logout.html")