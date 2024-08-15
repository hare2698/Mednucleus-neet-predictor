from config import mongoconn 
import uuid

def validate(username,password):
    query = {"email":username,"password":password}
    cross_check = mongoconn().Users.find_one(query,{'_id':0})
    print(cross_check)
    return True if bool(cross_check) else False
        
def user_append(**kwargs):
    student_info={}
    for key,value in kwargs.items():
        if key == "student_name":
            student_info["name"] = value
        if key == "mark":
            student_info["mark"] = value
        if key == "zone":
            student_info["state"] = value
        if key == "sex":
            student_info["sex"] = value
        if key == "unique_id":
            student_info["unique_id"] = value
        if key == "Course":
            student_info["Course"] = value
        if key == "Category":
            student_info["Category"] = value
        if key == "Quota":
            student_info["Quota"] = value
    add_data = mongoconn().student_data.insert_one(student_info)
    return True if bool(add_data) else False

def get_student_data(unique_id):
    query = {"unique_id": unique_id}
    fetch_data = mongoconn().student_data.find(query,{"_id":0})
    print(fetch_data)
    if bool(fetch_data):
        return fetch_data
    else:
        return None

def user_edit(**kwargs):
    student_info={}
    for key,value in kwargs.items():
        if key == "student_name":
            student_info["name"] = value
        if key == "mark":
            student_info["mark"] = value
        if key == "state":
            student_info["state"] = value
        if key == "sex":
            student_info["sex"] = value
        if key == "unique_id":
            student_info["unique_id"] = value
        if key == "Course":
            student_info["Course"] = value
        if key == "Category":
            student_info["Category"] = value
        if key == "Quota":
            student_info["Quota"] = value
    query ={"unique_id":student_info["unique_id"]}
    fetch_data = mongoconn().student_data.update_one(query,{'$set':student_info})
    print(fetch_data)
    return True if bool(fetch_data) else False

def get_all_data():  
    fetch_data = mongoconn().student_data.find()
    print({"l":fetch_data})
    if bool(fetch_data):
        return fetch_data
    else:
        return None
    
def get_college_data(name):
    query = {"Institute":name}
    fetch_data = mongoconn().sample_raw_data.find(query,{"_id":0})
    if bool(fetch_data):
        return fetch_data
    else:
        return None
    