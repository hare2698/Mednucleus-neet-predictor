import pymongo

def mongoconn():
    mongoconn=pymongo.MongoClient('mongodb+srv://hare:Bbuulleett8@mednucleus.ax9wr8c.mongodb.net/?retryWrites=true&w=majority&appName=Mednucleus',connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    db = mongoconn["Neet_predictor"]                               
    return db

client=pymongo.MongoClient('mongodb+srv://hare:Bbuulleett8@mednucleus.ax9wr8c.mongodb.net/?retryWrites=true&w=majority&appName=Mednucleus',connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db =client["Neet_predictor"]

first_page = "/home/ubuntu/Mednucleus-neet-predictor/static/First_Page.png"
mid_page = "/home/ubuntu/Mednucleus-neet-predictor/static/Mid_Pages.png"
last_page = "/home/ubuntu/Mednucleus-neet-predictor/static/Last_Page.png"