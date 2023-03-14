from flask import redirect, render_template, request, session, flash
from functools import wraps
from application import APP
from application.utils import hash_string, process_login, sanitise_string
from application.utils import list_mds, md_to_html, delete_md, get_md, overwrite_md
from application.utils import get_settings_data, update_settings_data

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@APP.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if process_login(request.form.get('username'), request.form.get('password')):
            session['user'] = request.form.get('username')
            return redirect("/", code=302)
        else:
            flash("Invalid username and/or password!")
            return render_template("login.html")
    elif request.method == "GET" or session.get("user") is None:
        return render_template("login.html")

@APP.route("/logout")
@login_required
def logout():
    session["user"] = None
    return redirect("/", code=302)

@APP.route("/")
@login_required
def index():
    return render_template("index.html", menu=list_mds(), data=None)

@APP.route("/<string:var>", methods=['GET'])
@login_required
def article(var):
    if var not in list_mds():
        return redirect("/error")
    return render_template("article.html", menu=list_mds(), page={"title":var, "content": md_to_html(var)})

@APP.route("/delete/<string:var>", methods=["GET", "POST"])
@login_required
def delete(var):
    if request.method == "POST":
        delete_md(var)
        flash(f"Successfully deleted '{var}'.")
        return redirect("/", code=302)
    else:
        return redirect(f"/{var}", code=302)

@APP.route("/edit/<string:var>", methods=["GET", "POST"])
@login_required
def edit(var):
    if var not in list_mds():
        return redirect("/error", code=404)
    if request.method == "GET": # For getting to the edit page directly
        return render_template("edit.html", menu=list_mds(), page={"title":var, "content": get_md(var)})
    else: # For submitting the edit
        overwrite_md(var, request.form.get('title'), request.form.get('content'))
        sanitised_title = sanitise_string(request.form.get('title'))
        flash(f"Successfully saved '{sanitised_title}'.")
        return redirect(f"/{sanitised_title}")

@APP.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        return render_template("edit.html", menu=list_mds(), page=None)
    if request.method == "POST":
        overwrite_md(None, request.form.get('title'), request.form.get('content'))
        sanitised_title = sanitise_string(request.form.get('title'))
        flash(f"Successfully saved '{sanitised_title}'.")
        return redirect(f"/{sanitised_title}", code=302)

@APP.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "GET":
        return render_template("settings.html", menu=list_mds(), data=get_settings_data())
    else:
        # check password validity
        if not process_login(session["user"], request.form.get('current_password')):
            flash("Incorrect password was entered!")
            return redirect('/settings')
        # check matching passwords
        elif not request.form.get('confirm_new_password') == request.form.get('new_password'):
            flash("New passwords do not match!")
            return redirect('/settings')
        # commit changes (if any)
        update_settings_data(request.form.get('username'), request.form.get('new_password'), request.form.get('directory'))
        flash("Your details have been updates successfully!")
        return redirect('/settings')

@APP.route("/error")
def error():
    return render_template("error.html")
