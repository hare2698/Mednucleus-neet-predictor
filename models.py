from config import mongoconn 
from user_validate import get_filter_college_data
def ranking_field(total_rank,query):
    predictor={}
    college_data={}
    for rank in total_rank:
        for name,weight in rank.items():
            if name in predictor:
                predictor[name] +=weight
            else:
                predictor[name] = weight
    
    sorted_colleges= sorted(predictor.items(),key = lambda x: x[1],reverse=True)
    college_names = [colleges[0] for colleges in sorted_colleges]
    for x in college_names:
        user_data = get_filter_college_data(x,query)
        user_data = list(user_data)
       
        college_data[x]= len(user_data)
    
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
     
        
        if value =="Beds" or (value =="None" and occurance_bed["bed"]==0):           
            
            if value == "None":
                weightage=0.01
               
            else:
                weightage = priority_set(field)
            bed ={} 
            for data in fetch_data: 
                                          
                if data["Beds"] >= 0 and data["Beds"] <= 100 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*1
                    
                if data["Beds"] >= 101 and data["Beds"] <= 200 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*2               
                    
                if data["Beds"] >= 201 and data["Beds"] <= 300 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*3
                if data["Beds"] >= 301 and data["Beds"] <= 400 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*4
                if data["Beds"] >= 401 and data["Beds"] <= 500 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*5 
                if data["Beds"] >= 501 and data["Beds"] <= 600 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*6 
                if data["Beds"] >= 601 and data["Beds"] <= 700 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*7 
                if data["Beds"] >= 701 and data["Beds"] <= 800 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*8 
                if data["Beds"] >= 801 and data["Beds"] <= 900 :
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*9  
                
                if data["Beds"] >= 1001:
                    bed[data["Institute"]+"|"+data["Course"]] = weightage*10             
            bed_l.append(bed)
            occurance_bed["bed"]=1
            
       
        
        if value =="Rank" or (value =="None" and occurance_rank["rank"]==0) :
            if value == "None":
                weightage=0.01
            else:
                weightage = priority_set(field)                   
            
            rank={}
            for data in fetch_data:
                                                                     
                if data["Rank"] >= 0 and data["Rank"] <= 1000:               
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*10               
                    
                if data["Rank"] >= 1001 and data["Rank"] <= 2000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*9               
                
                if data["Rank"] >= 2001 and data["Rank"] <= 3000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*8 
                if data["Rank"] >= 3001 and data["Rank"] <= 4000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*7 
                if data["Rank"] >= 4001 and data["Rank"] <= 5000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*6
                if data["Rank"] >= 5001 and data["Rank"] <= 6000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*5
                if data["Rank"] >= 6001 and data["Rank"] <= 7000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*4 
                if data["Rank"] >= 7001 and data["Rank"] <= 8000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*3 
                if data["Rank"] >= 8001 and data["Rank"] <= 9000:
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*2 
                if data["Rank"] >= 10000 :
                    rank[data["Institute"]+"|"+data["Course"]] = weightage*1 
                           
            rank_l.append(rank)
            occurance_rank["rank"]=1
            
    
       
        if value =="Bond Years" or (value =="None" and occurance_bondyear["bond year"]==0) : 
            if value == "None":
                weightage=0.01
            else:
                weightage = priority_set(field)                     
            
            Bond_year={}
            for data in fetch_data: 
                             
                if data["Bond Years"] >= 0 and data["Bond Years"] <= 10 :              
                    Bond_year[data["Institute"]+"|"+data["Course"]] = weightage*3             
                    
                if data["Bond Years"] >= 10 and data["Bond Years"] <= 15:
                    Bond_year[data["Institute"]+"|"+data["Course"]] = weightage*2             
                    
                if data["Bond Years"] >= 15 :
                    Bond_year[data["Institute"]+"|"+data["Course"]] = weightage*1
                              
            Bond_year_l.append(Bond_year)
            occurance_bondyear["bond year"]=1
            
        
               
        if value =="Fee" or (value =="None" and occurance_fee["fee"]==0):    
            if value == "None":
                weightage=0.01
            else:
                weightage = priority_set(field)        
            
            fee={}
            for data in fetch_data:
                                                 
                if type(data["Fee"])=="string":
                    fees=data["Fee"].replace(",","")
                else:
                    fees=data["Fee"]
                if fees >= 0 and fees <= 100000 :
                                 
                    fee[data["Institute"]+"|"+data["Course"]] = weightage*3             
                    
                if fees >= 10000 and fees<= 1000000:
                    fee[data["Institute"]+"|"+data["Course"]] = weightage*2             
                    
                if fees >= 1000000 :
                    fee[data["Institute"]+"|"+data["Course"]] = weightage*1               
            fee_l.append(fee)
            occurance_fee["fee"]=1
            
        
        
        if value =="Stipend Year 1" or (value =="None" and occurance_stipend["stipend"]==0) :
            if value == "None":
                weightage=0.01
            else:
                weightage = priority_set(field)           
           
            stipend_year={}
            for data in fetch_data: 
                          
                if data["Stipend Year 1" ] >= 0 and data["Stipend Year 1" ] <= 10000 :              
                    stipend_year[data["Institute"]+"|"+data["Course"]] = weightage*1             
                    
                if data["Stipend Year 1" ] >= 10001 and data["Stipend Year 1" ] <= 20000:
                    stipend_year[data["Institute"]+"|"+data["Course"]] = weightage*2             
                    
                if data["Stipend Year 1" ] >= 20001 and data["Stipend Year 1" ] <= 30000:
                    stipend_year[data["Institute"]+"|"+data["Course"]] = weightage*3            
                    
                if data["Stipend Year 1" ] >= 30001 and data["Stipend Year 1" ] <= 40000:
                    stipend_year[data["Institute"]+"|"+data["Course"]] = weightage*4            
                    
                if data["Stipend Year 1" ] >= 40001 and data["Stipend Year 1" ] <= 50000:
                    stipend_year[data["Institute"]+"|"+data["Course"]]= weightage*5            
                   
                if data["Stipend Year 1" ] >= 50001:
                    stipend_year[data["Institute"]+"|"+data["Course"]] = weightage*6 
                            
            stipend_year_1_l.append(stipend_year)
            occurance_stipend["stipend"]=1
            
       
       
        if value =="Bond Penalty" or (value =="None" and occurance_bond_penality["bond penality"]==0):
            if value == "None":
                weightage=0.01
            else:
                weightage = priority_set(field)           
            
            bond_penality={}
            for data in fetch_data: 
                           
                if data["Bond Penalty"] >= 0 and data["Bond Penalty"] <= 100000 :              
                    bond_penality[data["Institute"]+"|"+data["Course"]] = weightage*3            
                    
                if data["Bond Penalty"] >= 100000 and data["Bond Penalty"] <= 300000:
                    bond_penality[data["Institute"]+"|"+data["Course"]] = weightage*2             
                    
                if data["Bond Penalty"] >= 300000 :
                    bond_penality[data["Institute"]+"|"+data["Course"]] = weightage*1 
                             
            bond_penality_l.append(bond_penality) 
            occurance_bond_penality["bond penality"]=1  
              
        

    total_rank = bed_l+rank_l+ bond_penality_l + Bond_year_l +fee_l+stipend_year_1_l
   
    rank_prediction = ranking_field(total_rank,query)
    return rank_prediction

def filter_data(filter_1,filter_2,filter_3,filter_4):
    query =  {"State":{"$in":filter_2[0]},"Course":{"$in":filter_3[0]},"Category":{"$in":filter_1[0]},"Quota":{"$in":filter_4[0]}}
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
    
    return list(fetch_data)