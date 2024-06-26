from flask import Blueprint, session, render_template, redirect, flash, request
import sqlite3

logins = Blueprint("login", __name__)


@logins.route("/")
@logins.route("/signup", methods=["GET", "POST"])
def signup():
    cx = sqlite3.connect("ToDo.db")
    cursor = cx.cursor()
    if request.method == "GET":
        return render_template("signup.html")
    username_tuple = request.form.get("username")
    if not username_tuple:
        flash("Invalid username!!")
        return redirect("/signup")
    username = username_tuple
    if len(username) < 4:
        flash(f"Username {username} is too short!!")
        return redirect("/signup")
    cursor.execute("INSERT INTO users(username) VALUES (?)", (username, ))
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username, ))
    user_id = cursor.fetchone()
    if not user_id:
        flash("Insertion of your username failed miserably😶")
    session["user_id"] = user_id
    cx.commit()
    return redirect("/list")


@logins.route("/login", methods=["GET", "POST"])
def login():
    cx = sqlite3.connect("ToDo.db")
    cursor = cx.cursor()
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    if not username:
        flash("Invalid username!!")
        return redirect("/login")
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username, ))
    user_id = cursor.fetchone()
    if not user_id:
        flash("You are not signed up yet")
        return redirect("/signup")
    flash(f"Welcome back {username}!!")
    return redirect("/list")
