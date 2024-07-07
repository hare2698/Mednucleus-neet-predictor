import pymongo

def mongoconn():
    mongoconn=pymongo.MongoClient('mongodb+srv://harekishans:Mednucleus08@mednucleus.xq7zaxn.mongodb.net/?retryWrites=true&w=majority&appName=Mednucleus')
    db = mongoconn["Mednucleus"]                               
    return db