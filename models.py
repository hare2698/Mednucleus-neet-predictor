from config import mongoconn 

def ranking_field(total_rank):
    predictor={}
    for rank in total_rank:
        for name,weight in rank.items():
            if name in predictor:
                predictor[name] +=weight
            else:
                predictor[name] = weight
    print(predictor)
    sorted_colleges= sorted(predictor.items(),key = lambda x: x[1],reverse=True)
    college_names = [colleges[0] for colleges in sorted_colleges]
    return college_names

def prediction_logic(**kwargs):
    bed_l=[]
    rank_l=[]
    size_l=[]
    print(kwargs.items())
    for field,value in kwargs.items():
        print(field,value)
        if field =="bed" and value =="on":          
            query =  { field: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:
                    bed ={}
                    if data[field] >= 0 and data[field] <= 300 :
                        bed[data["name"]] = 1
                        bed_l.append(bed)
                    if data[field] >= 300 and data[field] <= 600 :
                        bed[data["name"]] = 2               
                        bed_l.append(bed)
                    if data[field] >= 600 :
                        bed[data["name"]] = 3                
                        bed_l.append(bed)
        print({"bed":bed_l})
        if field =="rank" and value =="on":
            query =  { field: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:          
                rank={}
                if data[field] >= 5 and data[field] <= 10 :               
                    rank[data["name"]] = 1                
                    rank_l.append(rank)
                if data[field] >= 2 and data[field] <= 5:
                    rank[data["name"]] = 2               
                    rank_l.append(rank)
                if data[field] <= 1 :
                    rank[data["name"]] = 3              
                    rank_l.append(rank)
        print({"rank":rank_l})
        if field =="size" and value =="on":
            query =  { field: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:       
                size={}
                if data[field] >= 0 and data[field] <= 300 :              
                    size[data["name"]] = 1             
                    size_l.append(size)
                if data[field] >= 301 and data[field] <= 600:
                    size[data["name"]] = 2             
                    size_l.append(size)
                if data[field] >= 600 :
                    size[data["name"]] = 3               
                    size_l.append(size)
        print({"size":size_l})
    total_rank = bed_l+rank_l+size_l
    rank_prediction = ranking_field(total_rank)
    return rank_prediction

prediction_logic
