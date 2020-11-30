from MovieData import MovieData
from pymongo import MongoClient
import json
import os

client = MongoClient()
db = client['IR']
collection = db['Movies']
directory_path="/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/index-t/IR"
for filename in os.listdir(directory_path):

    if ".txt" not in filename:
        continue
    # combining the path names
    file_path = os.path.join(directory_path, filename)
    print(file_path)
    current_doc = MovieData(file_path)
    if current_doc.data_ast is not None:        
     title=current_doc.get("title")
     overview=current_doc.get("overview")
     genres=current_doc.get("genres")
     genres=json.dumps(genres)
    
##    genre="{"+genres[0]['name']
##    for i in genres[1:]:
##     genre=genre+", "+i['name']
##    genre=genre+"}"
##    print(genre)
    #genres=current_doc.get("genres")
    #print(genres[0]['name'])
     try:
      json_obj=json.loads("{\"title\":\""+current_doc.get("title")+"\" ,\"overview\":\""+current_doc.get("overview")+"\" ,\"genre\":"+genres+"}")
      print(json_obj)
      movies_id = collection.insert_one(json_obj)
     except ValueError:
      print ('Decoding JSON has failed')
			
