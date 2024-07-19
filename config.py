import pymongo

def mongoconn():
    mongoconn=pymongo.MongoClient('mongodb+srv://hare:Bbuulleett8@mednucleus.ax9wr8c.mongodb.net/?retryWrites=true&w=majority&appName=Mednucleus',connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    db = mongoconn["Neet_predictor"]                               
    return db