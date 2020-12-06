import os
from os.path import join as pjoin
import json

BASE_ADDRESS = "https://api.themoviedb.org/3/movie/"
API_KEY = "?api_key=d06ee9d17787be31829956793ca3e36b"

# name_emb = {'e': '5555', 'f': '6666'}

output_dir = '/Users/panda/Desktop/movie_1202'

movies = os.listdir(output_dir)
for movie in movies:
    if movie.split(".")[1] != "json":
        continue
    movie_id = movie.split('_')[1].split('.')[0]
    actorUrl = BASE_ADDRESS + movie_id + "/credits" + API_KEY
    imageUrl = BASE_ADDRESS + movie_id + "/images" + API_KEY
    urls = {'actorUrl': actorUrl, 'imageUrl': imageUrl}
    fr = open(output_dir+"/"+movie)
    # print(movie)
    # print(movie_id)
    model = json.load(fr)
    fr.close()

    for i in urls:
        model[i] = urls[i]

    jsObj = json.dumps(model)

    with open(output_dir+"/"+movie, "w") as fw:
        fw.write(jsObj)
        fw.close()