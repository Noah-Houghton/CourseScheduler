# Implements a backend for a website allowing users to submit, search, and manage posts with administrative functionality for specific users

import SQL
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

crs_db = SQL("sqlite:///courses.db")
prof_db = SQL("sqlite:///professors.db")
COS_db = SQL("sqlite:///concentrations.db")
usr_db = SQL("sqlite:///users.db")

@app.route("/", methods = ["GET", "POST"])
@login_required
def home():
    """Home page, displays current courseload and requirements"""
    crs_rows = crs_db.execute("SELECT * WHERE cid in :active", active = usr_db.execute("SELECT cid FROM active"))
    COS_rows = COS_db.execute("SELECT * WHERE id = :userCOS", userCOS = usr_db.execute("SELECT COS WHERE active = True"))
    return render_template("home.html", crs_data = crs_rows, COS_data = COS_rows)