from config import mongoconn 
from user_validate import get_filter_college_data
from user_validate import priority_data

def ranking_field(total_rank,query,priority):
    predictor={}
    college_data={}
    for rank in total_rank:
        for name,weight in rank.items():
            if name in predictor:
                predictor[name] +=weight
            else:
                predictor[name] = weight
    
    sorted_colleges= sorted(predictor.items(),key = lambda x: x[1],reverse=True)

    for colleges in sorted_colleges:      
        p_data=priority_data(colleges[0].split(" | ")[0])[0]
        user_data = get_filter_college_data(colleges[0],query)
        user_data = list(user_data)
        college_data[colleges[0]+"_"+str(round(colleges[1],7))+"_"+str(p_data["Fee"])+"_"+str(p_data["Bond Penalty"])+"_"+str(p_data["Bond Years"])+"_"+str(p_data["Beds"])+"_"+str(p_data["Stipend Year 1"])]= len(user_data)
    print({"col_data":college_data})
    
    if priority!="None":
    # Sorting function
        value = priority_value_set(priority)
        sorted_items = sorted(college_data.items(), key=lambda item: (float(item[0].split('_')[1]),int(item[0].split('_')[value])),reverse=True)
    
    # Creating a sorted dictionary (if needed)
        sorted_dict = {key: value for key, value in sorted_items}
        print({"sorted****************":sorted_dict})
        return sorted_dict
    return college_data

def prediction_logic(*args,**kwargs):
    arg={}
    bed_l=[]
    rank_l=[]
    Bond_year_l=[]
    bond_penality_l=[]
    fee_l=[]
    stipend_year_1_l=[]
    count=0
    occurance_bed={"bed":count}
    occurance_stipend={"stipend":count}
    occurance_bond_penality={"bond penality":count}
    occurance_rank={"rank":count}
    occurance_bondyear={"bond year":count}
    occurance_fee={"fee":count}
    
    fetch_data = args[0]
    query=args[1]
    for field,value in kwargs.items():
        if field=="priority_1":
            priority=value
        print(field,value)
        
        if value =="Beds" or (value =="None" and occurance_bed["bed"]==0):           
            
            if value == "None":
                weightage=0
               
            else:
                weightage = priority_set(field)
            bed ={} 
            for data in fetch_data: 
                                          
                if data["Beds"] >= 0 and data["Beds"] <= 200 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*1
                    
                if data["Beds"] >= 201 and data["Beds"] <= 400 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*2               
                    
                if data["Beds"] >= 401 and data["Beds"] <= 600 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*3
                if data["Beds"] >= 601 and data["Beds"] <= 800 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*4
                if data["Beds"] >= 801 and data["Beds"] <= 1000 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*5 
                if data["Beds"] >= 1001 and data["Beds"] <= 1200 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*6 
                if data["Beds"] >= 1201 and data["Beds"] <= 1400 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*7 
                if data["Beds"] >= 1401 and data["Beds"] <= 1600 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*8 
                if data["Beds"] >= 1601 and data["Beds"] <= 1800 :
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*9  
                
                if data["Beds"] >= 1801:
                    bed[data["Institute"]+" | "+data["Course"]] = weightage*10             
            bed_l.append(bed)
            occurance_bed["bed"]=1
            
        print({"bed":bed_l})
        
        if value =="Rank" or (value =="None" and occurance_rank["rank"]==0) :
            if value == "None":
                weightage=0
            else:
                weightage = priority_set(field)                   
            
            rank={}
            for data in fetch_data:
                                                                     
                if data["Rank"] >= 0 and data["Rank"] <= 2500:               
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*10               
                    
                if data["Rank"] >= 2501 and data["Rank"] <= 5000:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*9               
                
                if data["Rank"] >= 5001 and data["Rank"] <= 7500:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*8 
                if data["Rank"] >= 7501 and data["Rank"] <= 10000:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*7 
                if data["Rank"] >= 10001 and data["Rank"] <= 12500:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*6
                if data["Rank"] >= 12501 and data["Rank"] <= 15000:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*5
                if data["Rank"] >= 15001 and data["Rank"] <= 17500:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*4 
                if data["Rank"] >= 17501 and data["Rank"] <= 20000:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*3 
                if data["Rank"] >= 20001 and data["Rank"] <= 25000:
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*2 
                if data["Rank"] >= 25001 :
                    rank[data["Institute"]+" | "+data["Course"]] = weightage*1 
                           
            rank_l.append(rank)
            occurance_rank["rank"]=1
            
        print({"rank":rank_l})
       
        if value =="Bond Years" or (value =="None" and occurance_bondyear["bond year"]==0) : 
            if value == "None":
                weightage=0
            else:
                weightage = priority_set(field)                     
            
            Bond_year={}
            for data in fetch_data: 
                             
                if data["Bond Years"] >= 0 and data["Bond Years"] <= 0.9:              
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*10            
                    
                if data["Bond Years"] >= 1 and data["Bond Years"] <= 1.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*9            
                    
                if data["Bond Years"] >= 2 and data["Bond Years"] <= 2.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*8
                
                if data["Bond Years"] >= 3 and data["Bond Years"] <= 3.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*7
                
                if data["Bond Years"] >= 4 and data["Bond Years"] <= 4.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*6
                if data["Bond Years"] >= 5 and data["Bond Years"] <= 5.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*5
                if data["Bond Years"] >= 6 and data["Bond Years"] <= 6.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*4
                if data["Bond Years"] >= 7 and data["Bond Years"] <= 7.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*3
                if data["Bond Years"] >= 8 and data["Bond Years"] <= 8.9:
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*2
                if  data["Bond Years"] >= 9 :
                    Bond_year[data["Institute"]+" | "+data["Course"]] = weightage*1
                              
            Bond_year_l.append(Bond_year)
            occurance_bondyear["bond year"]=1
            
        print({"Bond_year":Bond_year_l})
               
        if value =="Fee" or (value =="None" and occurance_fee["fee"]==0):    
            if value == "None":
                weightage=0
            else:
                weightage = priority_set(field)        
            
            fee={}
            for data in fetch_data:
                                                 
                if type(data["Fee"])=="string":
                    fees=data["Fee"].replace(",","")
                else:
                    fees=data["Fee"]
                if fees >= 0 and fees <= 20000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*10            
                    
                if fees >= 20001 and fees<= 40000:
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*9            
                    
                if fees >= 40001 and fees<= 60000:
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*8  
                if fees >= 60001 and fees <= 80000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*7
                if fees >= 80001 and fees <= 100000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*6 
                if fees >= 100001 and fees <= 120000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*5
                if fees >= 120001 and fees <= 140000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*4 
                if fees >= 140001 and fees <= 160000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*3 
                if fees >= 160001 and fees <= 180000 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*2 
                if fees >= 180001 :
                                 
                    fee[data["Institute"]+" | "+data["Course"]] = weightage*1  
                          
            fee_l.append(fee)
            occurance_fee["fee"]=1
            
        print({"fee":fee_l})
        
        if value =="Stipend Year 1" or (value =="None" and occurance_stipend["stipend"]==0) :
            if value == "None":
                weightage=0
            else:
                weightage = priority_set(field)           
           
            stipend_year={}
            for data in fetch_data: 
                          
                if data["Stipend Year 1" ] >= 0 and data["Stipend Year 1" ] <= 13000 :              
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*1             
                    
                if data["Stipend Year 1" ] >= 13001 and data["Stipend Year 1" ] <= 26000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*2             
                    
                if data["Stipend Year 1" ] >= 26001 and data["Stipend Year 1" ] <= 39000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*3            
                    
                if data["Stipend Year 1" ] >= 39001 and data["Stipend Year 1" ] <= 52000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*4            
                    
                if data["Stipend Year 1" ] >= 52001 and data["Stipend Year 1" ] <= 65000:
                    stipend_year[data["Institute"]+" | "+data["Course"]]= weightage*5            
                   
                if data["Stipend Year 1" ] >= 65001 and data["Stipend Year 1" ] <= 78000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*6 

                if data["Stipend Year 1" ] >= 78001 and data["Stipend Year 1" ] <= 91000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*7
                if data["Stipend Year 1" ] >= 91001 and data["Stipend Year 1" ] <= 104000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*8
                if data["Stipend Year 1" ] >= 104001 and data["Stipend Year 1" ] <= 117000:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*9
                if data["Stipend Year 1" ] >= 117001:
                    stipend_year[data["Institute"]+" | "+data["Course"]] = weightage*10
                 
                            
            stipend_year_1_l.append(stipend_year)
            occurance_stipend["stipend"]=1
            
        print({"stipend":stipend_year_1_l})
       
        if value =="Bond Penalty" or (value =="None" and occurance_bond_penality["bond penality"]==0):
            if value == "None":
                weightage=0
            else:
                weightage = priority_set(field)           
            
            bond_penality={}
            for data in fetch_data: 
                           
                if data["Bond Penalty"] >= 0 and data["Bond Penalty"] <= 500000 :              
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*10           
                    
                if data["Bond Penalty"] >= 500001 and data["Bond Penalty"] <= 1000000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*9            
                    
                if data["Bond Penalty"] >= 1000001 and data["Bond Penalty"] <= 1500000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*8
                if data["Bond Penalty"] >= 1500001 and data["Bond Penalty"] <= 2000000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*7 
                if data["Bond Penalty"] >= 2000001 and data["Bond Penalty"] <= 2500000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*6 
                if data["Bond Penalty"] >= 2500001 and data["Bond Penalty"] <= 3000000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*5 
                if data["Bond Penalty"] >= 3000001 and data["Bond Penalty"] <= 3500000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*4 
                if data["Bond Penalty"] >= 3500001 and data["Bond Penalty"] <= 4000000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*3 
                if data["Bond Penalty"] >= 4000001 and data["Bond Penalty"] <= 4500000:
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*2 
                if data["Bond Penalty"] >= 4500001 :
                    bond_penality[data["Institute"]+" | "+data["Course"]] = weightage*1 
                
                             
            bond_penality_l.append(bond_penality) 
            occurance_bond_penality["bond penality"]=1  
              
        print({"Bond_penality":bond_penality_l})

    total_rank = bed_l+rank_l+ bond_penality_l + Bond_year_l +fee_l+stipend_year_1_l
    print({"total_rank":total_rank})
    rank_prediction = ranking_field(total_rank,query,priority)
    return rank_prediction

def filter_data(filter_1,filter_2,filter_3,filter_4):
    query =  {"State":{"$in":filter_2[0]},"Course":{"$in":filter_3[0]},"Category":{"$in":filter_1[0]},"Quota":{"$in":filter_4[0]}}
    print(query)
    fetch_data = mongoconn().sample_raw_data.find(query,{'_id':0})
    
    fetch_data = list(fetch_data)
    return fetch_data,query

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
            weightage = 0.025
    return weightage

def distinct_data(value):
    fetch_data = mongoconn().sample_raw_data.distinct(value)
    print(list(fetch_data))
    return list(fetch_data)

def personal_rankings(data,query):
    personal_rank={}
    college_data={}
    for college in data:
        try:
            personal_rank[college["Institute"] + " | " +college["Course"]]=college["KM Ranking"]
        except Exception as e:
            personal_rank[college["Institute"] + " | " +college["Course"]]=9999
    sorted_colleges= sorted(personal_rank.items(),key = lambda x: x[1])
    college_names = [colleges[0]+"_"+str(colleges[1] if colleges[1]!=9999 else "Yet to be Ranked") for colleges in sorted_colleges]
    print(college_names)
    for college in college_names:
        name=college.split("_")[0]
        user_data = get_filter_college_data(name,query)
        college_data[college]= len(list(user_data))
        
    return college_data

def priority_value_set(value):
    if value=="Beds":
        return 5
    if value=="Fee":
        return 2
    if value=="Stipend Year 1":
        return 6
    if value=="Bond Penalty":
        return 3
    if value=="Bond Years":
        return 4
    return 5
