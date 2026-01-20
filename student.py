import os
from flask import Flask,request,render_template
app=Flask(__name__,template_folder='templates')
import sqlite3
DB_PATH = "/tmp/student.db"
def init_db():
    conn=sqlite3.connect(DB_PATH)
    c=conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS student
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    marks INTEGER NOT NULL)
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/")
def index():
    return render_template("student.html")
    
@app.route("/add_student", methods=["GET","POST"])
def add_student():
    message=""
    if request.method=="POST":
        name=request.form.get("student_name")
        marks=request.form.get("student_marks")
        conn=sqlite3.connect(DB_PATH)
        c=conn.cursor()
        c.execute("insert into student (name,marks)values(?,?)",(name,marks))
        conn.commit()
        conn.close()
        message="added successfully"
    return render_template("student.html", message=message)

@app.route("/viws_student", methods=["GET","POST"])
def viws_student():
    conn=sqlite3.connect(DB_PATH)
    c=conn.cursor()
    c.execute("select name,marks from student")
    students_list=c.fetchall()
    conn.commit()
    conn.close()
    return render_template("viws.html", students=students_list)

@app.route("/update_student", methods=["GET","POST"])
def update_student():
    message=""
    if request.method=="POST":
        name=request.form.get("student_name")
        update_marks=request.form.get("update_marks")
        conn=sqlite3.connect(DB_PATH)
        c=conn.cursor()
        c.execute("update student set marks=? where name=?",(update_marks,name))
        if c.rowcount >0:
            message="student marks updated successfully"
        else:
            message="student not found"
        conn.commit()
        conn.close()
    return render_template("update.html", message=message)

@app.route("/delete_student", methods=["GET","POST"])
def delete_student():
    message=""
    if request.method=="POST":
        name=request.form.get("delete_student")
        conn=sqlite3.connect(DB_PATH)
        c=conn.cursor()
        c.execute("delete from student where name=?",(name,))
        if c.rowcount >0:
            message="delete student successfully"
        else:
            message="student not found"
        conn.commit()
        conn.close()
    return render_template("delete.html", message=message)
if __name__ =="__main__":
    port =int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0' , port=port)




