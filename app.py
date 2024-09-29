from flask import Flask,render_template,request,abort,jsonify,request,redirect,url_for,flash,session,send_file
from io import BytesIO
from fpdf import FPDF
import json
import pandas as pd
from user_validate import validate,user_append,get_student_data,user_edit,get_all_data,get_college_data,student_record_insert
import pymongo
from models import prediction_logic,filter_data,distinct_data
from datetime import datetime, timedelta
import ast
import tempfile
import ast


app=Flask(__name__)

app.secret_key ="wjbdvjkwb=kjvbwkvnlqkvj;lql;"
# Set the timeout period
TIMEOUT = timedelta(seconds=10)  # 10 seconds

def data_clean(data):
   conv_list=[data]
   return conv_list

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
         flash("invalid creds please try again", "error")
         return render_template("welcome.html")  
   return render_template("welcome.html")

@app.route("/Predictor_hub", methods = ["GET","POST"])
def Predictor_hub():
   if request.method == "POST":    
      unique_id = request.form.get("unique_id")
      print(unique_id)
      fetch_student_data = get_student_data(unique_id)
      data = list(fetch_student_data)
      print(data)
      if type(data[0]["State"]) is not list:
         data[0]["State"]=[(data[0]["State"])]
         
      if type(data[0]["Course"]) is not list:
         data[0]["Course"]=[(data[0]["Course"])]
         
      if type(data[0]["Quota"]) is not list:
         data[0]["Quota"]=[(data[0]["Quota"])]
        
      if type(data[0]["Category"]) is not list:
         data[0]["Category"]=[(data[0]["Category"])]
         
     
      filter_1= [datas["Category"] for datas in data]
      filter_2= [datas["State"] for datas in data]
      filter_3= [datas["Course"] for datas in data]
      filter_4= [datas["Quota"] for datas in data]
     
      p1_field= request.form.get("priority-1") if request.form.get("priority-1") else 0   
      p2_field= request.form.get("priority-2") if request.form.get("priority-2") else 0
      p3_field= request.form.get("priority-3") if request.form.get("priority-3") else 0
      p4_field= request.form.get("priority-4") if request.form.get("priority-4") else 0
      p5_field= request.form.get("priority-5") if request.form.get("priority-5") else 0
      p6_field= request.form.get("priority-6") if request.form.get("priority-6") else 0
      preference_dict={"p1":p1_field,"p2":p2_field,"p3":p3_field,"p4":p4_field,"p5":p5_field,"p6":p6_field}
      if len(data) == 0:
         return render_template("thankyou.html",message = "Please enter a valid ID",flag=False)
      if  bool(fetch_student_data) and p1_field == 0 and p2_field == 0 and p3_field == 0 and p4_field == 0 and p5_field == 0 and p6_field == 0:
         return render_template("predictor_hub.html",data=data,data_type="list",map="from predictor hub")
      else :
         
         datas,query = filter_data(filter_1,filter_2,filter_3,filter_4)
        
         predicted_data = prediction_logic(datas,query,priority_1=p1_field,priority_2=p2_field,priority_3=p3_field,priority_4=p4_field,priority_5=p5_field,priority_6=p6_field)
      if not predicted_data:
         return render_template("thankyou.html",message = f"sorry, No data has been found on the given combination <br><br> category = {filter_1[0]}<br> state = {filter_2[0]}<br>course = {filter_3[0]}<br>Quota = {filter_4[0]} ",flag=False)
      else:
         merged_stu_college_detail=student_record_insert(data[0] | {"selected_colleges":[predicted_data]} | {"preference":preference_dict})
         return render_template("sorted_colleges_names.html",data=predicted_data,filter_data=query,unique_id=unique_id,student_data=data,preference=preference_dict)
      
   return render_template("welcome.html")

@app.route("/student_operation", methods = ["GET","POST"])
def student_operation():
   if request.method == "POST": 
      operation = request.form.get("operation")
      
      if operation == "create registration":
         state_data = distinct_data("State")
         course_data =distinct_data("Course") 
         Quota_data = distinct_data("Quota")
         category_data=distinct_data("Category")
         return render_template("student_registration.html",state=state_data,course=course_data,quota=Quota_data,category=category_data)
      elif operation == "edit registration":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)

         return render_template("student_edit_registration_form.html",unique_id=None,data=data)
      elif operation == "fetch registration":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
        
         return render_template("predictor_hub.html",data=data,data_type="list",map="from operation")
      elif operation == "NEET predictor":
         user_data = get_all_data().sort("created_at",pymongo.DESCENDING)
         data = list(user_data)
         return render_template("predictor_hub.html",data=data,data_type="list",map="from operation")
      else:
         user_data = get_college_data(operation)
         user_data = list(user_data)
        
         unique_id= request.form.get("student_data")      
         fetch_student_data = get_student_data(unique_id)
         data = list(fetch_student_data)
         
         #filter_data=ast.literal_eval(filter_data)
         print({"user_data":user_data})
         return render_template("college_list.html",data=user_data,data_type="list",map="college_result",student_data=data)
   return render_template("welcome.html")

@app.route("/student_registration", methods = ["GET","POST"])
def student_registration():
   if request.method == "POST": 
     
      add_student_data = user_append(student_name=request.form.get("name"),mark=request.form.get("mark"),sex=request.form.get("sex"),zone=request.form.getlist("zone"),unique_id =request.form.get("id"),Course=request.form.getlist("Course"),Quota=request.form.getlist("Quota"),Category=request.form.getlist("Category"),education=request.form.get("education"),email=request.form.getlist("email"),contact=request.form.getlist("contact_number"),languages=request.form.getlist("languages"))
      if add_student_data == True:
         data ={}
         data["Name"]=request.form.get("name")
         data["Sex"]=request.form.get("sex")
         data["Zone"]=request.form.getlist("zone")
         data["Mark"]=request.form.get("mark")
         data["unique_id"]=request.form.get("id")
         data["Category"]=request.form.getlist("Category")
         data["Course"]=request.form.getlist("Course")
         data["Quota"]=request.form.getlist("Quota")
         data["Email"]=request.form.get("email")
         data["Contact_Details"]=request.form.get("contact_number")
         data["Languages"]=request.form.get("languages")
         data["Education_Details"]=request.form.get("education")
         return render_template("predictor_hub.html" ,data = data,data_type = "dict")
      else:
         return render_template("thankyou.html" ,message = " Please check unique ID uniqueness if the problem persists, there might be an database issue Try again later" )
   return render_template("welcome.html")

@app.route("/student_registration_update", methods = ["GET","POST"])
def student_registration_update():
   if request.method == "POST": 
      state_data = distinct_data("State")
      course_data =distinct_data("Course") 
      Quota_data = distinct_data("Quota")
      category_data=distinct_data("Category")
      fetch_student_data = None
      unique_id = request.form.get("unique_id") 
      if unique_id is None: 
         return render_template("student_edit_registration_form.html",unique_id=None)
      fetch_student_data = get_student_data(unique_id)
      
      data = list(fetch_student_data) 
      
      if  len(data) != 0:
         return render_template("student_edit_registration_form.html",unique_id=unique_id,data=data,data_type="list",state=state_data,course=course_data,quota=Quota_data,category=category_data)
      else:
         return render_template("thankyou.html",message = "Please enter a valid ID",flag=False)
   return render_template("welcome.html")

@app.route("/student_registration_update_display", methods = ["GET","POST"])
def student_registration_update_display():
   if request.method == "POST":  
      edit_student_data = user_edit(student_name=request.form.get("Name"),mark=request.form.get("Mark"),sex=request.form.get("Sex"),state=request.form.getlist("zone"),unique_id=request.form.get("unique_id"),Course=request.form.getlist("Course"),Quota=request.form.getlist("Quota"),Category=request.form.getlist("Category"),education=request.form.getlist("education"),email=request.form.getlist("email"),contact=request.form.getlist("contact"),languages=request.form.getlist("language"))
      if edit_student_data == True:
         data ={}
         data["Name"]=request.form.get("Name")
         data["Sex"]=request.form.get("Sex")
         data["Zone"]=request.form.getlist("zone")
         data["Mark"]=request.form.get("Mark")
         data["unique_id"]=request.form.get("unique_id")
         data["Category"]=request.form.getlist("Category")
         data["Course"]=request.form.getlist("Course")
         data["Quota"]=request.form.getlist("Quota")
         data["Email"]=request.form.get("email")
         data["Contact_Details"]=request.form.get("contact")
         data["Languages"]=request.form.get("language")
         data["Education_Details"]=request.form.get("education")
         return render_template("predictor_hub.html" ,data = data,data_type = "dict")
      else:
         flash("there was a error in editing a data please try again later",'error')
         return render_template("student_edit_registration_form.html" ,message = "student registration" )
   return render_template("welcome.html")

@app.route('/download_pdf',methods = ["GET","POST"])
def download_pdf():
    if request.method == "POST": 
      # Create a PDF document
      pdf = FPDF()
      pdf.add_page()
      pdf.set_fill_color(230, 230, 230) 
      pdf.set_font("Arial", size = 12)
      
      # Example table data
      table_data = request.form.get("data_input")
      table_data=ast.literal_eval(table_data)
      data=request.form.get("student_data")
      data =ast.literal_eval(data)
     
      # Add table headers
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(50, 10,"Registered Student Details")
      pdf.ln()
      pdf.set_font("Arial", size = 12)
      for values in data:
         for k,v in values.items():
            if k=="unique_id":
               unique_id=v
            pdf.cell(25, 10, k, border=1)
            if type(v) is list:
                     pdf.multi_cell(0, 10, ", ".join(v), border=1)  # Use multi_cell for wrapping, adjust height as needed
            else:
                     pdf.cell(0, 10, v, border=1) 
                     pdf.ln()
      pdf.add_page()
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(50, 10,"College Seat Details")
      pdf.ln()
      pdf.set_font("Arial", size=12)
      pdf.cell(50, 20,"College Parameters", border=1)
      pdf.cell(100, 20, "Details", border=1)
      pdf.ln()

      # Add table rows
      pdf.set_font("Arial", size = 12)
      
      length = len(table_data)
  
      count=0
      for row in table_data:
         count=count+1
         for k,v in row.items():
            if k=="Institute":
               c_n=v
            if k=="Course":
               course=v
            pdf.cell(50, 10,f"{k}", border=1)
            pdf.cell(100, 10,f"{v}", border=1)
            pdf.ln()
         pdf.ln()
    
         if count ==len(table_data):
            break
         pdf.add_page()
         pdf.set_font("Arial", size=12)
         pdf.cell(50, 20,"College Parameters", border=1)
         pdf.cell(100, 20, "Details", border=1)
         pdf.ln()

      # Save the PDF to a BytesIO object

      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
         pdf.output(temp_file.name)
         temp_file.seek(0)
         return send_file(temp_file.name, as_attachment=True, download_name=f"{unique_id+'_'+c_n+'_'+course}.pdf", mimetype='application/pdf')
    return render_template("welcome.html") 

@app.route('/download_pdf_list',methods = ["GET","POST"])
def download_pdf_list():
    if request.method == "POST": 
      # Create a PDF document
      unique_id = request.form.get("student_data") 
   
      fetch_student_data = get_student_data(unique_id)
      data = list(fetch_student_data)
   
      pdf = FPDF()
      pdf.add_page()
      pdf.set_font("Arial", size = 12)
      # Example table data
      table_data = request.form.get("data_input")
      table_data=ast.literal_eval(table_data)
      
      # Add table headers
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(40, 10,"Registered Student Details")
      pdf.ln()
      for value in data:
          for k,v in value.items():
            if k=="unique_id":
               unique_id=v
            pdf.cell(25, 10, k, border=1)
            if type(v) is list:
                     pdf.multi_cell(0, 10, ", ".join(v), border=1)  # Use multi_cell for wrapping, adjust height as needed
            else:
                     pdf.cell(0, 10, v, border=1) 
                     pdf.ln()
      pdf.add_page()
      pdf.cell(40, 10,"Personalised College Mapping")
      pdf.ln()
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(25, 10,"Order", border=1)
      pdf.cell(120, 10, "College Name", border=1)
      pdf.cell(25, 10, "No of Seats", border=1)
      pdf.ln()

      # Add table rows
      pdf.set_font("Arial", size = 12)
      count =0
      for key,value in table_data.items():
         key=key.split("_")[0]
         count+=1
         pdf.cell(25, 10,str(count), border=1)
         pdf.cell(120, 10,key, border=1)
         pdf.cell(25, 10,str(value), border=1)
         pdf.ln()

      # Save the PDF to a BytesIO object

      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
         pdf.output(temp_file.name)
         temp_file.seek(0)
         return send_file(temp_file.name, as_attachment=True, download_name=f'{unique_id+"_"+"college_list"}.pdf', mimetype='application/pdf')
    return render_template("welcome.html")     
if __name__=="__main__":
   app.run(debug=True)