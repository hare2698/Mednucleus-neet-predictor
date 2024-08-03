from flask import Flask,render_template,request,abort,jsonify,request,redirect,url_for,flash,session,send_file
from io import BytesIO
from fpdf import FPDF
import json
import pandas as pd
from user_validate import validate,user_append,get_student_data,user_edit,get_all_data,get_college_data
import pymongo
from models import prediction_logic
from datetime import datetime, timedelta
import ast
import tempfile

app=Flask(__name__)

app.secret_key ="wjbdvjkwb=kjvbwkvnlqkvj;lql;"
# Set the timeout period
TIMEOUT = timedelta(seconds=10)  # 10 seconds


@app.route("/welcome")
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
            user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
            data = list(user_data)
            return render_template("predictor_hub.html",data=data,data_type="list",map="from operation")
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
         return render_template("predictor_hub.html",data=data,data_type="list",map="from predictor hub")
   return render_template("welcome.html")

@app.route("/student_operation", methods = ["GET","POST"])
def student_operation():
   if request.method == "POST": 
      operation = request.form.get("operation")
      if operation == "create registration":
         return render_template("student_registration.html")
      elif operation == "edit registration":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
         return render_template("student_edit_registration_form.html",unique_id=None,data=data)
      elif operation == "fetch registration":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
         print({"dh":data})
         return render_template("predictor_hub.html",data=data,data_type="list",map="from operation")
      elif operation == "NEET predictor":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
         return render_template("predictor_hub.html",data=data,data_type="list",map="from operation")
      else:
         user_data = get_college_data(operation)
         data = list(user_data)
         print(user_data)
         return render_template("college_list.html",data=data,data_type="list",map="college_result")
   return render_template("welcome.html")

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
         data["unique_id"]=request.form.get("id")
         return render_template("predictor_hub.html" ,data = data,data_type = "dict")
      else:
         flash("there was a error in adding a data please try again later",'error')
         return render_template("student_registration.html" ,message = "student registration" )
   return render_template("welcome.html")

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

@app.route("/prediction_algorithm", methods = ["GET","POST"])
def prediction_algorithm():
   if request.method == "POST":  
      p1_field= request.form.get("priority-1") if request.form.get("priority-1") else None   
      p2_field= request.form.get("priority-2") if request.form.get("priority-2") else None
      p3_field= request.form.get("priority-3") if request.form.get("priority-3") else None   
      predicted_data = prediction_logic(priority_1=p1_field,priority_2=p2_field,priority_3=p3_field)
      return render_template("sorted_colleges_names.html",data=predicted_data)
   return render_template("welcome.html")
@app.route('/download_pdf',methods = ["GET","POST"])
def download_pdf():
    if request.method == "POST": 
      # Create a PDF document
      pdf = FPDF()
      pdf.add_page()
      pdf.set_font("Arial", size = 12)
      
      # Example table data
      table_data = request.form.get("data_input")
      print(table_data)
      table_data=ast.literal_eval(table_data)
      print(table_data)
      # Add table headers
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(40, 10,"Please find your college details")
      pdf.ln()
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(40, 10,"college parameters", border=1)
      pdf.cell(40, 10, "value", border=1)
      pdf.ln()

      # Add table rows
      pdf.set_font("Arial", size = 12)
      for row in table_data:
         for k,v in row.items():
            pdf.cell(40, 10,f"{k}", border=1)
            pdf.cell(40, 10,f"{v}", border=1)
            pdf.ln()

      # Save the PDF to a BytesIO object

      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
         pdf.output(temp_file.name)
         temp_file.seek(0)
         return send_file(temp_file.name, as_attachment=True, download_name='customized_data.pdf', mimetype='application/pdf')
    return render_template("welcome.html")    
if __name__=="__main__":
   app.run(debug=True)