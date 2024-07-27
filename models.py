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
        if value =="bed" :
            print("insdie bed")
            if field=="priority_1":
                 weightage = 0.5
            if field=="priority_2":
                 weightage = 0.3
            if field=="priority_3":
                 weightage = 0.2
            query =  { value: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:
                    bed ={}
                    if data[value] >= 0 and data[value] <= 300 :
                        bed[data["name"]] = weightage*1
                        bed_l.append(bed)
                    if data[value] >= 300 and data[value] <= 600 :
                        bed[data["name"]] = weightage*2               
                        bed_l.append(bed)
                    if data[value] >= 600 :
                        bed[data["name"]] = weightage*3                
                        bed_l.append(bed)
        print({"bed":bed_l})
        if value =="rank" :
            if field=="priority_1":
                 weightage = 0.5
            if field=="priority_2":
                 weightage = 0.3
            if field=="priority_3":
                 weightage = 0.2
            query =  { value: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:          
                rank={}
                if data[value] >= 5 and data[value] <= 10 :               
                    rank[data["name"]] = weightage*1               
                    rank_l.append(rank)
                if data[value] >= 2 and data[value] <= 5:
                    rank[data["name"]] = weightage*2               
                    rank_l.append(rank)
                if data[value] <= 1 :
                    rank[data["name"]] = weightage*3              
                    rank_l.append(rank)
        print({"rank":rank_l})
        if value =="size":
            if field=="priority_1":
                 weightage = 0.5
            if field=="priority_2":
                 weightage = 0.3
            if field=="priority_3":
                 weightage = 0.2
            query =  { value: { "$exists": True }}
            fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
            fetch_data = list(fetch_data)
            for data in fetch_data:       
                size={}
                if data[value] >= 0 and data[value] <= 300 :              
                    size[data["name"]] = weightage*1             
                    size_l.append(size)
                if data[value] >= 301 and data[value] <= 600:
                    size[data["name"]] = weightage*2             
                    size_l.append(size)
                if data[value] >= 600 :
                    size[data["name"]] = weightage*3               
                    size_l.append(size)
        print({"size":size_l})
    total_rank = bed_l+rank_l+ size_l
    rank_prediction = ranking_field(total_rank)
    return rank_prediction


 