from flask import redirect, render_template, request, session, url_for
from functools import wraps
import sqlite3
import urlparse
import json

crs_db = sqlite3.connect("courses.db")
prof_db = sqlite3.connect("professors.db")
COS_db = sqlite3.connect("concentrations.db")
snd_db = sqlite3.connect("secondaries.db")
lng_db = sqlite3.connect("languages.db")
sctn_db = sqlite3.connect("sections.db")
# active courses are stored as a jsonified list of course ids which must be looked up in crs_db
# gened requirements stored as a jsonified dict
usr_db = sqlite3.connect("users.db")

crs_c = crs_db.cursor()
prof_c = prof_db.cursor()
COS_c = COS_db.cursor()
snd_c = snd_db.cursor()
sctn_c = sctn_db.cursor()
usr_c = usr_db.cursor()

# adds a course to the courses database
def addCourse(ID, name, abv, description, profID, isSeminar, dept, credType, numCreds=4, qScore=0):
    # this must be updated if column order or contents changes
    crs_c.execute("INSERT INTO Courses VALUES (:ID, :name, :abv, :description, :profID, :isSem, :dept, :cred, :numC, :q)", ID = ID, name = name, abv = abv, description = description, profID = profID, isSem = isSeminar, dept = dept, cred = credType, numC = numCreds, q = qScore)

# deletes the course matching ID
def deleteCourse(ID):
    crs_c.execute("DELETE * FROM Courses WHERE ID=:ID", ID=ID)

# returns the list of courses a student has designated as active
def activeCourses(student_id):
    try:
        # get ids of active courses as a dumped json string
        courseIDs = usr_c.execute("SELECT Courses FROM Students WHERE ID=?", (student_id,))
        # load dumped string into list of integers
        idList = json.loads(courseIDs)
        # prepare list for SQL query
        ids = '(' + ','.join(map(str, idList)) + ')'
        # return the list of courses which are in the student's active list
        return crs_c.execute("SELECT * FROM Courses WHERE ID in ?", (ids,))
    except:
        return []

# returns the course whose ID matches cid
def lookupCourse(cid):
    return crs_c.execute("SELECT * FROM Courses WHERE ID=:id", id=cid)

# returns the CoS currently selected by the student
def activeCOS(student_id):
    try:
        # get identifier of student's CoS as a dumped json string
        # json string allows for one or more concentrations to be selected
        cosIDs = json.loads(usr_c.execute("SELECT Conc FROM Students WHERE ID=?", (student_id,)))
        # get secondary identifier
        sndID = usr_c.execute("SELECT Snd FROM Students WHERE ID=?", (student_id,))
        # get language identifier
        lngID = usr_c.execute("SELECT Lng FROM Students WHERE ID=?", (student_id,))

        # prepare IDs for SQL query
        cosids = '(' + ','.join(map(str, cosIDs)) + ')'

        COS = COS_c.execute("SELECT * FROM CoursesOfStudy WHERE ID in ?", (cosids,))

        SND = snd_c.execute("SELECT * FROM Secondaries WHERE ID=?", (sndID[0],))

        LNG = lng_c.execute("SELECT * FROM Languages WHERE ID=:lngID", (lngID[0],))

        # return data as a dictionary for easy access
        return {"COS" : COS, "SND" : SND, "LNG" : LNG}
    except:
        return {"COS" : [], "SND" : [], "LNG" : []}

# sets the student's COS, SND, and LNG based on params
# if None, then no change. Must be "NONE" to remove
def setCOS(student_id, COS_ID=None, SND_ID=None, LNG_ID=None):
    if COS_ID != None:
        usr_c.execute("UPDATE Students SET COS=:COS_ID WHERE ID=:student_id", COS_ID = COS_ID, student_id = student_id)
    elif SND_ID != None:
        usr_c.execute("UPDATE Students SET SND=:SND_ID WHERE ID=:student_id", SND_ID = SND_ID, student_id = student_id)
    elif LNG_ID != None:
        usr_c.execute("UPDATE Students SET LNG=:LNG_ID WHERE ID=:student_id", LNG_ID = LNG_ID, student_id = student_id)

# adds a course to a student's active roster
def activateCourse(ID, S_ID):
    # get ids of active courses as a dumped json string
    courseIDs = usr_c.execute("SELECT Courses FROM Students WHERE ID=:student_id", student_id = student_id)
    # load dumped string into list of integers
    current = json.loads(courseIDs)
    new = json.dumps(current.append(ID))
    usr_c.execute("UPDATE Students SET Courses=:new WHERE ID=:S_ID", new = new, S_ID = S_ID)

# removes a course from a student's active roster
def deactivateCourse(ID, S_ID):
    # get ids of active courses as a dumped json string
    courseIDs = usr_c.execute("SELECT Courses FROM Students WHERE ID=:student_id", student_id = student_id)
    # load dumped string into list of integers
    current = json.loads(courseIDs)
    new = json.dumps(current.remove(ID))
    usr_c.execute("UPDATE Students SET Courses=:new WHERE ID=:S_ID", new = new, S_ID = S_ID)

# sets a course's professor
def setProf(ID, P_ID):
    # can use this to see which professors teach which courses without maintaining a separate list
    # for each prof, run SELECT * FROM Courses WHERE Professor=this.P_ID
    crs_c.execute("UPDATE Courses SET Professor=:P_ID WHERE ID=:ID", P_ID = P_ID, ID = ID)

# returns the data of the professor who teaches this course
def getProf(ID):
    return crs_c.execute("SELECT Professor FROM Courses WHERE ID=:ID", ID = ID)

# returns the professor who matches P_ID
def lookupProf(P_ID):
    return prof_c.execute("SELECT * FROM Professors WHERE ID=:P_ID", P_ID = P_ID)

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
def admin_required(f):
    """
    Decorate routes to require admin login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        rows = db.execute("SELECT user_id FROM users WHERE admin='True' AND user_id=:uid", uid = session.get("user_id"))
        if not rows:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s