from flask import Flask,render_template,request,abort,jsonify,request,redirect,url_for,flash
from models import db,save_db
import json
import pandas as pd
from user_validate import validate,user_append,get_student_data,user_edit,get_all_data
import pymongo

app=Flask(__name__)

app.secret_key ="wjbdvjkwb=kjvbwkvnlqkvj;lql;"

@app.route("/")
def introduction():  
   return render_template("welcome.html")

@app.route("/login", methods = ["GET","POST"])
def login():
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      operation = request.form.get("operation")
      user_validation = validate(username,password)
      if user_validation == True:
         flash('Login success', 'success')
         if operation == "student_registration":
            return render_template("student_operation.html")
         else:
            return render_template("predictor_hub.html",data=None)
      else: 
         flash("invalid creds please try agian", "error")
         return render_template("welcome.html")  
   return render_template("welcome.html")

@app.route("/Predictor_hub", methods = ["GET","POST"])
def Predictor_hub():
   if request.method == "POST":    
      fetch_student_data = None
      unique_id = request.form.get("unique_id")  
      fetch_student_data = get_student_data(unique_id)
      data = list(fetch_student_data) 
      if len(data) == 0:
         return render_template("thankyou.html",message = "Please enter a valid ID",flag=False)
      if  bool(fetch_student_data):
         return render_template("predictor_hub.html",data=data,data_type="list")
   return render_template("welcome.html")

@app.route("/student_operation", methods = ["GET","POST"])
def student_operation():
   if request.method == "POST": 
      operation = request.form.get("operation")
      if operation == "create registration":
         return render_template("student_registration.html")
      if operation == "edit registration":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
         return render_template("student_edit_registration_form.html",unique_id=None,data=data)
      if operation == "fetch registration":
         return render_template("predictor_hub.html",data=None)
      if operation == "NEET predictor":
         return render_template("predictor_hub.html",data=None)
   return render_template("student_operation.html")

@app.route("/student_registration", methods = ["GET","POST"])
def student_registration():
   if request.method == "POST": 
      add_student_data = user_append(student_name=request.form.get("name"),mark=request.form.get("mark"),sex=request.form.get("sex"),zone=request.form.get("zone"),unique_id =request.form.get("ID"))
      if add_student_data == True:
         data ={}
         data["name"]=request.form.get("name")
         data["sex"]=request.form.get("sex")
         data["zone"]=request.form.get("zone")
         data["mark"]=request.form.get("mark")
         return render_template("predictor_hub.html" ,data = data,data_type = "dict")
      else:
         flash("there was a error in adding a data please try again later",'error')
         return render_template("student_registration.html" ,message = "student registration" )
   return render_template("student_operation.html")

@app.route("/student_registration_update", methods = ["GET","POST"])
def student_registration_update():
   if request.method == "POST": 
      fetch_student_data = None
      unique_id = request.form.get("unique_id") 
      if unique_id is None: 
         return render_template("student_edit_registration_form.html",unique_id=None)
      fetch_student_data = get_student_data(unique_id)
      data = list(fetch_student_data) 
      if  len(data) != 0:
         return render_template("student_edit_registration_form.html",unique_id=unique_id,data=data,data_type="list")
      else:
         return render_template("thankyou.html",message = "Please enter a valid ID",flag=False)
   return render_template("welcome.html")

@app.route("/student_registration_update_display", methods = ["GET","POST"])
def student_registration_update_display():
   if request.method == "POST":  
      edit_student_data = user_edit(student_name=request.form.get("name"),mark=request.form.get("mark"),sex=request.form.get("sex"),zone=request.form.get("zone"),unique_id=request.form.get("unique_id"))
      if edit_student_data == True:
         data ={}
         data["name"]=request.form.get("name")
         data["sex"]=request.form.get("sex")
         data["zone"]=request.form.get("zone")
         data["mark"]=request.form.get("mark")
         data["unique_id"]=request.form.get("unique_id")
         return render_template("predictor_hub.html" ,data = data,data_type = "dict")
      else:
         flash("there was a error in editing a data please try again later",'error')
         return render_template("student_edit_registration_form.html" ,message = "student registration" )
   return render_template("welcome.html")


if __name__=="__main__":
   app.run(debug=True)