from flask import render_template, request, redirect, session

from estusshots import app
from estusshots.util import authorize, get_user_type


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        user_type = get_user_type(request.form.get("password"))
        if not user_type:
            return redirect("/login")
        session["user_type"] = user_type
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("role", None)
    return redirect("login")


@app.route("/")
@authorize
def landing():
    return redirect("/season")
