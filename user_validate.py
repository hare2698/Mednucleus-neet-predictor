from config import mongoconn,db
from datetime import datetime,timedelta,timezone
import time

def validate(password,operation):
    if operation == "agent_login":
        query = {"secret_key":str(password)}
        cross_check = db.agent_login.find_one(query,{'_id':0})     
    else:
        query = {"secret_key":str(password)}
        cross_check = mongoconn().secret_keys.find_one(query,{'_id':0})
        if not bool(cross_check):
            cross_check = mongoconn().secret_keys.insert_one(query,{'_id':0})
        
    return True if bool(cross_check) else False

def download_review():
    try:
        review = db.reviews.find().sort( "created_dt", -1 ).limit(1)
        review=list(review)
    except:
        review =None
    return review
        
   
    

    
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

def priority_data(name):
    query = {"Institute":name}
    collection=db.sample_raw_data
    fetch_data = collection.find(query,{"_id":0,"Fee":1,"Stipend Year 1":1,"Bond Penalty":1,"Bond Years":1,"Beds":1})
    fetch_data = list(fetch_data)
    if bool(fetch_data):
        return fetch_data
    else:
        return None

def upload_token(values,operation):
    if operation == "token":
        data=[]
        for token in values:
            data.append({"secret_key":token})
        try:
            upload = db.secret_keys.insert_many(data)
        except Exception:
            upload = False
        return bool(upload)
    else:
        dt_object = datetime.now(timezone.utc)
        data = {"created_dt":dt_object,"reviews":values}
        upload = db.reviews.insert_one(data)
        return bool(upload)
    
