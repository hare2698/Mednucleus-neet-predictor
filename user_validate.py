from config import mongoconn,db
from datetime import datetime
import time

def validate(username,password):
    query = {"email":username,"password":password}
    cross_check = mongoconn().Users.find_one(query,{'_id':0})
   
    return True if bool(cross_check) else False
        
def user_append(**kwargs):
    student_info={}
    for key,value in kwargs.items():    
        if key == "student_name":
            student_info["Name"] = value
        if key == "mark":
            student_info["Mark"] = value
        if key == "zone":
            student_info["State"] = value
        if key == "sex":
            student_info["Sex"] = value
        if key == "unique_id":
            student_info["unique_id"] = value
        if key == "Course":
            student_info["Course"] = value
        if key == "Category":
            student_info["Category"] = value
        if key == "Quota":
            student_info["Quota"] = value
        if key == "email":
            student_info["Email"] = value
        if key == "languages":
            student_info["Language"] = value
        if key == "education":
            student_info["Education"] = value
        if key == "contact":
            student_info["Contact"] = value
    print({"student_info":student_info})
    try:
        add_data = mongoconn().student_data.insert_one(student_info)
        return True if bool(add_data) else False
    except Exception as e:
        return False

def get_student_data(unique_id):
    query = {"unique_id": unique_id}
    fetch_data = mongoconn().student_data.find(query,{"_id":0})
    if bool(fetch_data):
        return fetch_data
    else:
        return None

def user_edit(**kwargs):
    student_info={}
    for key,value in kwargs.items():
        if key == "student_name":
            student_info["Name"] = value
        if key == "mark":
            student_info["Mark"] = value
        if key == "state":
            student_info["State"] = value
        if key == "sex":
            student_info["Sex"] = value
        if key == "unique_id":
            student_info["unique_id"] = value
        if key == "Course":
            student_info["Course"] = value
        if key == "Category":
            student_info["Category"] = value
        if key == "Quota":
            student_info["Quota"] = value
        if key == "email":
            student_info["Email"] = value
        if key == "languages":
            student_info["Language"] = value
        if key == "education":
            student_info["Education"] = value
        if key == "contact":
            student_info["Contact"] = value
    query ={"unique_id":student_info["unique_id"]}
    fetch_data = mongoconn().student_data.update_one(query,{'$set':student_info})
    print(fetch_data)
    return True if bool(fetch_data) else False

def get_all_data():  
    fetch_data = mongoconn().student_data.find()
    
    if bool(fetch_data):
        return fetch_data
    else:
        return None
    
def get_filter_college_data(query_college,query_filter):
    #query_filter=ast.literal_eval(query_filter)
    parsed_query = query_college.split(" | ") 
    
    course=parsed_query[1]
    college=parsed_query[0]
    match_filter={"$match":query_filter}
    college_course = {"$match":{"Institute":college,"Course":course,"Round":1}}
    query = [match_filter,college_course]
   
    collection=db.sample_raw_data
    fetch_data = collection.aggregate(query)
    if bool(fetch_data):
        return fetch_data
    else:
        return None
    
def get_college_data(name):
    #query_filter=ast.literal_eval(query_filter)
    parsed_query = name.split(" | ") 
    course=parsed_query[1]
    college=parsed_query[0]
    query = {"Institute":college,"Course":course}
    collection=db.sample_raw_data
    fetch_data = collection.find(query,{"_id":0})
    if bool(fetch_data):
        return fetch_data
    else:
        return None
    
def student_record_insert(student_info):
    current_timestamp = time.time()
    dt_object = datetime.fromtimestamp(current_timestamp)
    formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    student_info["date_time"]=formatted_date
    add_data = mongoconn().student_preferred_college.insert_one(student_info)
    return True if bool(add_data) else False