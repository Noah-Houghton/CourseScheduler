from flask import redirect, render_template, request, session, url_for
from functools import wraps
import SQL
import urllib.parse

crs_db = SQL("sqlite:///courses.db")

def lookup(query, keys):
    """Looks up entries based on keywords and/or content string"""
    # if no keyword provided, allow all
    ids = []
    if keys:
        keywords = keys.split(";")
        print("keyword list: ", end="")
        print(keywords)
        for word in keywords:
            rows = db.execute("SELECT ids FROM keywords WHERE keyword LIKE :key", key = '%' + word + '%')
            if rows:
                sql_ids = rows[0]["ids"]
                posts = sql_ids.split(";")
                for i in posts:
                    ids.append(int(i))
    if ids:
            sql_query = 'SELECT * FROM content WHERE ' + ' OR '.join(('id = ' + str(n) for n in ids))
            rows = db.execute(sql_query)
            if not rows:
                rows = db.execute("SELECT * FROM content WHERE id=:pid AND canRead = 'True'", pid = ids[0])
    
    if query:
        # search database content for query
        rows2 = db.execute("SELECT * FROM content WHERE (content LIKE :content OR title LIKE :title) AND canRead = 'True'", content = '%' + query + '%', title = '%' + query + '%')
    #return items that match word AND keywords
    if query and keys:
        final = combineDicts(rows, rows2)
    # return items that match word
    elif query:
        final = rows2
    # return items that match keywords
    elif keys:
        final = rows
    # no query, no keys
    else:
        final = db.execute("SELECT * FROM content WHERE canRead = 'True'")
    # return items
    return [{"title": item["title"], "content": item["content"], "post_id": item["id"], "uid": item["user_id"], "username": item["username"]} for item in final]

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

# admin helper methods
def delete(uname):
    # delete user
    db.execute("DELETE FROM users WHERE username = :name", name = uname)

def changeAdmin(b, uname):
    # if b is true, box was checked
    if b:
        db.execute("UPDATE users SET admin = 'True' WHERE username = :name", name = uname)
    # if b is false, box was not checked
    else:
        db.execute("UPDATE users SET admin = 'False' WHERE username = :name", name = uname)
