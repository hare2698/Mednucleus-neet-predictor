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

def prediction_logic(*args,**kwargs):
    bed_l=[]
    rank_l=[]
    Bond_year_l=[]
    bond_penality_l=[]
    fee_l=[]
    stipend_year_1_l=[]
    for data in args:
        fetch_data=data
    print(kwargs.items())    
    for field,value in kwargs.items():
        print(field,value)
        if value =="Beds" :
            print("insdie bed")
            weightage = priority_set(field)
            for data in fetch_data:
                
                bed ={}
                if data[value] >= 0 and data[value] <= 500 :
                    bed[data["Institute"]] = weightage*1
                    bed_l.append(bed)
                if data[value] >= 500 and data[value] <= 1000 :
                    bed[data["Institute"]] = weightage*2               
                    bed_l.append(bed)
                if data[value] >= 1000 :
                    bed[data["Institute"]] = weightage*3                
                    bed_l.append(bed)
        print({"bed":bed_l})
        if value =="Rank" :
            weightage = priority_set(field)
            for data in fetch_data:                       
                rank={}
                if data[value] >= 0 and data[value] <= 100:               
                    rank[data["Institute"]] = weightage*3               
                    rank_l.append(rank)
                if data[value] >= 100 and data[value] <= 1000:
                    rank[data["Institute"]] = weightage*2               
                    rank_l.append(rank)
                if data[value] <= 1000 :
                    rank[data["Institute"]] = weightage*1             
                    rank_l.append(rank)
        print({"rank":rank_l})
        if value =="Bond Years":
            weightage=priority_set(field)
            for data in fetch_data:
                      
                Bond_year={}
                if data[value] >= 0 and data[value] <= 10 :              
                    Bond_year[data["Institute"]] = weightage*3             
                    Bond_year_l.append(Bond_year)
                if data[value] >= 10 and data[value] <= 15:
                    Bond_year[data["Institute"]] = weightage*2             
                    Bond_year_l.append(Bond_year)
                if data[value] >= 15 :
                    Bond_year[data["Institute"]] = weightage*1               
                    Bond_year_l.append(Bond_year)
        print({"Bond_year":Bond_year_l})
        if value =="Fee":
            weightage=priority_set(field)
            for data in fetch_data:                      
                fee={}
                fees=data[value].replace(",","")
                fees=int(fees)
                if fees >= 0 and fees <= 100000 :              
                    fee[data["Institute"]] = weightage*3             
                    fee_l.append(fee)
                if fees >= 10000 and fees<= 1000000:
                    fee[data["Institute"]] = weightage*2             
                    fee_l.append(fee)
                if fees >= 1000000 :
                    fee[data["Institute"]] = weightage*1               
                    fee_l.append(fee)
        print({"fee":fee_l})
        if value =="Stipend Year 1":
            weightage=priority_set(field)
            for data in fetch_data:
                       
                stipend_year={}
                if data[value] >= 0 and data[value] <= 20000 :              
                    stipend_year[data["Institute"]] = weightage*1             
                    stipend_year_1_l.append(Bond_year)
                if data[value] >= 20000 and data[value] <= 50000:
                    stipend_year[data["Institute"]] = weightage*2             
                    stipend_year_1_l.append(Bond_year)
                if data[value] >= 50000 :
                    stipend_year[data["Institute"]] = weightage*3               
                    stipend_year_1_l.append(Bond_year)
        print({"stipend":stipend_year_1_l})
        if value =="Bond Penalty":
            weightage=priority_set(field)
            for data in fetch_data:
                       
                bond_penality={}
                if data[value] >= 0 and data[value] <= 100000 :              
                    bond_penality[data["Institute"]] = weightage*3            
                    bond_penality_l.append(Bond_year)
                if data[value] >= 100000 and data[value] <= 300000:
                    bond_penality[data["Institute"]] = weightage*2             
                    bond_penality_l.append(Bond_year)
                if data[value] >= 300000 :
                    bond_penality[data["Institute"]] = weightage*1              
                    bond_penality_l.append(bond_penality)       
        print({"Bond_penality":bond_penality_l})
    total_rank = bed_l+rank_l+ bond_penality_l + Bond_year_l +fee_l+stipend_year_1_l
    print({"total_rank":total_rank})
    rank_prediction = ranking_field(total_rank)
    return rank_prediction

def filter_data(filter_1,filter_2,filter_3,filter_4):
    
    query =  { "Category":filter_1[0],"Quota":filter_4[0],"State":filter_2[0],"Course":filter_3[0]}
    
    fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
    fetch_data = list(fetch_data)
    
    return fetch_data

def priority_set(field):
    if field=="priority_1":
         weightage = 0.50
    if field=="priority_2":
            weightage = 0.20
    if field=="priority_3":
            weightage = 0.15
    if field=="priority_4":
            weightage = 0.10
    if field=="priority_5":
            weightage = 0.05
    if field=="priority_6":
            weightage = 0.05
    return weightage