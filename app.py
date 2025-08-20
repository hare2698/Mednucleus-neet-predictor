from flask import Flask,render_template,request,abort,jsonify,request,redirect,url_for,flash,session,send_file
from io import BytesIO
from fpdf import FPDF
import json
import pandas as pd
from user_validate import validate,user_append,get_student_data,user_edit,get_all_data,get_college_data,student_record_insert
import pymongo
from models import prediction_logic,filter_data,distinct_data,personal_rankings
from datetime import datetime, timedelta
import ast
import tempfile
import ast
from config import mongoconn,db



app=Flask(__name__)

app.secret_key ="wjbdvjkwb=kjvbwkvnlqkvj;lql;"
# Set the timeout period
TIMEOUT = timedelta(seconds=10)  # 10 seconds

def data_clean(data):
   conv_list=[data]
   return conv_list

def data_type(data):
      if type(data[0]["State"]) is not list:
         data[0]["State"]=[(data[0]["State"])]
         
      if type(data[0]["Course"]) is not list:
         data[0]["Course"]=[(data[0]["Course"])]
         
      if type(data[0]["Quota"]) is not list:
         data[0]["Quota"]=[(data[0]["Quota"])]
        
      if type(data[0]["Category"]) is not list:
         data[0]["Category"]=[(data[0]["Category"])]

      return data
@app.route("/welcome")
def introduction():  
   return render_template("welcome.html")


@app.route("/login", methods = ["GET","POST"])
def login():
   if request.method == "POST":
      global password
      password = request.form.get("password")
      print(password)
      user_validation = validate(password)
      if user_validation == True:
         flash('Login success', 'success')
         state_data = distinct_data("State")
         course_data =distinct_data("Course") 
         Quota_data = distinct_data("Quota")
         category_data=distinct_data("Category")
         return render_template("predictor_hub.html",state=state_data,course=course_data,quota=Quota_data,category=category_data,data_type="list",map="from operation")
      else: 
         flash("Token might expired or invalid token entered", "error")
         return render_template("welcome.html")  
   return render_template("welcome.html")

@app.route("/Predictor_hub", methods = ["GET","POST"])
def Predictor_hub(): 
   if request.method == "POST":    
      filter_1=[request.form.getlist("Category")]
      filter_3=[request.form.getlist("Course")]
      filter_4=[request.form.getlist("Quota")]
      filter_2=[request.form.getlist("zone")]
     
      p1_field= request.form.get("priority-1") if request.form.get("priority-1") else 0   
      p2_field= request.form.get("priority-2") if request.form.get("priority-2") else 0
      p3_field= request.form.get("priority-3") if request.form.get("priority-3") else 0
      p4_field= request.form.get("priority-4") if request.form.get("priority-4") else 0
      p5_field= request.form.get("priority-5") if request.form.get("priority-5") else 0
      p6_field= request.form.get("priority-6") if request.form.get("priority-6") else 0
      preference_dict={"p1":p1_field,"p2":p2_field,"p3":p3_field,"p4":p4_field,"p5":p5_field,"p6":p6_field}
      # if p1_field == 0 and p2_field == 0 and p3_field == 0 and p4_field == 0 and p5_field == 0 and p6_field == 0:
      #    return render_template("predictor_hub.html",data=data,data_type="list",map="from predictor hub")
      # else :
         
      datas,query = filter_data(filter_1,filter_2,filter_3,filter_4)
        
      predicted_data = prediction_logic(datas,query,priority_1=p1_field,priority_2=p2_field,priority_3=p3_field,priority_4=p4_field,priority_5=p5_field,priority_6=p6_field)
      if not predicted_data:
         return render_template("thankyou.html",message = f"sorry, No data has been found on the given combination <br><br> category = {filter_1[0]}<br> state = {filter_2[0]}<br>course = {filter_3[0]}<br>Quota = {filter_4[0]} ",flag=False)
      else:
         merged_stu_college_detail=student_record_insert({"Token":password} | {"selected_colleges":[predicted_data]} | {"preference":preference_dict})
         return render_template("sorted_colleges_names.html",data=predicted_data,filter_data=query,preference=preference_dict)
      
   return render_template("welcome.html")

@app.route("/student_operation", methods = ["GET","POST"])
def student_operation():
   if request.method == "POST": 
      operation = request.form.get("operation")     
      user_data = get_college_data(operation)
      user_data = list(user_data)     
      #filter_data=ast.literal_eval(filter_data)
      print({"user_data":user_data})
      return render_template("college_list.html",data=user_data,data_type="list",map="college_result")
   return render_template("welcome.html")

@app.route('/download_pdf',methods = ["GET","POST"])
def download_pdf():
    if request.method == "POST": 
      # Create a PDF document
      pdf = FPDF()
      pdf.add_page()
      
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/First_Page.png",0,0,pdf.w,pdf.h)
      pdf.set_fill_color(230, 230, 230) 
      pdf.set_font("Arial", size = 12)
      pdf.set_text_color(255, 255, 255)
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
      # Example table data
      table_data = request.form.get("data_input")
      table_data=ast.literal_eval(table_data)
      college_name= request.form.get("college_name")
      print(college_name)
      course= request.form.get("course")
      bed= request.form.get("number of bed")
      fee=  request.form.get("college fee")
      bondyear= request.form.get("number of bondyear")
      penalty= request.form.get("penalty")
      stipend= request.form.get("stipend")
      # Add table headers
      pdf.set_font("Arial", size = 12)
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
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
      pdf.cell(50, 10,"Institute", border=1)
      pdf.cell(100, 10,college_name , border=1)
      pdf.ln()
      pdf.cell(50, 10,"Course", border=1)
      pdf.cell(100, 10,course , border=1)
      pdf.ln()
      pdf.cell(50, 10,"Bed", border=1)
      pdf.cell(100, 10,bed , border=1)
      pdf.ln()
      pdf.cell(50, 10,"Fees", border=1)
      pdf.cell(100, 10,fee, border=1)
      pdf.ln()
      pdf.cell(50, 10,"Bond Year", border=1)
      pdf.cell(100, 10,bondyear , border=1)
      pdf.ln()
      pdf.cell(50, 10,"Penalty", border=1)
      pdf.cell(100, 10,penalty , border=1)
      pdf.ln()
      pdf.cell(50, 10,"Stipend", border=1)
      pdf.cell(100, 10,stipend, border=1)
      pdf.ln()
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
      count=0
      for row in table_data:
         count=count+1
         for k,v in row.items():
            if k=="Institute":
               c_n=v
               continue
            if k=="Course":
               course=v
               continue
            if k=="Beds" or k=="Fee" or k=="Bond Years" or k=="Bond Penalty" or k=="Stipend Year 1":
               continue
            pdf.cell(50, 10,f"{k}", border=1)
            pdf.cell(100, 10,f"{v}", border=1)
            pdf.ln()
         pdf.ln()
    
         if count ==len(table_data):
            break
         pdf.add_page()
         pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
         pdf.set_font("Arial", size=12)
         pdf.cell(50, 20,"College Parameters", border=1)
         pdf.cell(100, 20, "Details", border=1)
         pdf.ln()
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Last_Page.png",0,0,pdf.w,pdf.h)
      # Save the PDF to a BytesIO object

      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
         pdf.output(temp_file.name)
         temp_file.seek(0)
         return send_file(temp_file.name, as_attachment=True, download_name=f"{password+'_'+c_n+'_'+course}.pdf", mimetype='application/pdf')
    return render_template("welcome.html") 

@app.route('/download_pdf_list',methods = ["GET","POST"])
def download_pdf_list():
    if request.method == "POST": 
      # Create a PDF document
      pwd_delete = mongoconn().secret_keys.delete_one({"secret_key":password})
      priority=request.form.get("priority")
      priority = ast.literal_eval(priority)
      print(type(priority))
      p_1=priority["p1"] if priority else "None"
      p_2=priority["p2"] if priority else "None"
      p_3=priority["p3"] if priority else "None"
      p_4=priority["p4"] if priority else "None"
      p_5=priority["p5"] if priority else "None"
      p_6=priority["p6"] if priority else "None"
   
      pdf = FPDF()
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/First_Page.png",0,0,pdf.w,pdf.h)
      pdf.add_page()
      pdf.set_text_color(255, 255, 255)
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
      pdf.set_font("Arial", size = 12)
      # Example table data
      table_data = request.form.get("data_input")
      table_data=ast.literal_eval(table_data)
      
      # Add table headers
      pdf.set_font("Arial", 'B', 12)
      pdf.cell(40, 10,"Registered Student Details")
      pdf.ln()
      pdf.cell(40, 10,"Student Preference")
      pdf.ln()
      pdf.cell(50, 10,"First priority", border=1)
      pdf.cell(50, 10, p_1, border=1)
      pdf.ln()
      pdf.cell(50, 10, "second priority", border=1)
      pdf.cell(50, 10, p_2, border=1)
      pdf.ln()
      pdf.cell(50, 10, "Third priority", border=1)
      pdf.cell(50, 10, p_3, border=1)
      pdf.ln()
      pdf.cell(50, 10, "Fourth priority", border=1)
      pdf.cell(50, 10, p_4, border=1)
      pdf.ln()
      pdf.cell(50, 10, "Fifth priority", border=1)
      pdf.cell(50, 10, p_5, border=1)
      pdf.ln()
      pdf.cell(50, 10, "sixth priority", border=1)
      pdf.cell(50, 10, p_6, border=1)
      pdf.ln()
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Mid_pages.png",0,0,pdf.w,pdf.h)
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
      pdf.add_page()
      pdf.image("C:/Users/hares/Downloads/Mednucleus/Mednucleus-neet-predictor/static/Last_Page.png",0,0,pdf.w,pdf.h)
      with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
         pdf.output(temp_file.name)
         temp_file.seek(0)
         return send_file(temp_file.name, as_attachment=True, download_name=f'{password+"_"+"college_list"}.pdf', mimetype='application/pdf')
    return render_template("welcome.html")    

@app.route('/custom_ranking',methods = ["GET","POST"])
def custom_ranking():
   if request.method == "POST":
      course=request.form.get("course")
      course=course.split(",")
      quota=request.form.get("quota")
      quota=quota.split(",")
      category=request.form.get("category")
      category=category.split(",")
      state=request.form.get("state")
      state=state.split(",")
      unique_id=request.form.get("unique_id")
      print(course,quota,state,unique_id)
      filterdata,query = filter_data([category],[state],[course],[quota])
      fetch_student_data = get_student_data(unique_id)
      data = list(fetch_student_data)
      
      preference_dict={"p1":'No Preference',"p2":'No Preference',"p3":'No Preference',"p4":'No Preference',"p5":'No Preference',"p6":'No Preference'}
      data=data_type(data)
      
      personalised_filter_data=personal_rankings(filterdata,query)
      print(personalised_filter_data)
      return render_template("sorted_colleges_names.html",data=personalised_filter_data,filter_data=query,unique_id=unique_id,student_data=data,preference=preference_dict)
if __name__=="__main__":

   app.run(host="0.0.0.0",port = 443,ssl_context=())
