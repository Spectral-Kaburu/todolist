from flask import session, redirect, render_template, flash, Blueprint, request
import sqlite3

stuffs = Blueprint('stuff', __name__)

@stuffs.route("/list", methods = ["GET", "POST"])
def lists():
    if "user_id" not in session:
        flash("You have not signed up!!")
        return redirect("/signup")
    cx = sqlite3.connect("ToDo.db")
    cursor = cx.cursor()
    user_id = session["user_id"]
    user_id = user_id[0]
    if request.method == "GET":
        cursor.execute("SELECT list_id, stuff, completed FROM list WHERE user_id = ?", (user_id, ))
        list = cursor.fetchall()
        if not list:
            flash("There are no tasks to be completed as of currently!!")
            pass
        return render_template("index.html", list = list)
    task = request.form.get("add")
    if not task:
        flash("No task was added!!")
        return redirect("/list")
    cursor.execute("INSERT INTO list(stuff, completed, user_id) VALUES (?, ?, ?)", (task, False, user_id))
    cursor.execute("SELECT list_id FROM list WHERE stuff = ?", (task, ))
    if not cursor.fetchone():
        flash("Insertion of your bogus task failed.")
        pass
    cx.commit()
    cursor.close()
    return redirect("/list")
    

@stuffs.route("/delete/<list_id>")
def delete(list_id):
    if "user_id" not in session:
        flash("You aren't signed up yet.")
        return redirect("/signup")
    cx = sqlite3.connect("ToDo.db")
    cursor = cx.cursor()
    cursor.execute("DELETE FROM list WHERE list_id = ?", (list_id, ))
    cx.commit()
    cursor.close()
    return redirect("/list")


@stuffs.route("/edit/<list_id>", methods=["GET", "POST"])
def edit(list_id):
    if "user_id" not in session:
        flash("You aren't signed up yet.")
        return redirect("/signup")
    cx = sqlite3.connect("ToDo.db")
    cursor = cx.cursor()
    cursor.execute("SELECT stuff FROM list WHERE list_id = ?", (list_id, ))
    task = cursor.fetchone()
    task = task[0]
    if request.method == "GET":
        return render_template("edit.html", task=task, list_id=list_id)
    edited_task = request.form.get("task")
    cursor.execute("UPDATE list SET stuff = ? WHERE list_id = ?", (edited_task, list_id, ))
    cx.commit()
    cursor.close()
    return redirect("/list")

