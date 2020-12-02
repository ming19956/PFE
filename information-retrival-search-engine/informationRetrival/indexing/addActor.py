# coding=utf-8
from pymongo import MongoClient
import json
import os

host = '127.0.0.1' # or localhost
port = 27017

myclient = MongoClient(host, port)
mydb = myclient['allMovies']
mycol = mydb["Movie"]

BASE_ADDRESS = "https://api.themoviedb.org/3/movie/"
API_KEY = "?api_key=d06ee9d17787be31829956793ca3e36b"

# https://api.themoviedb.org/3/movie/550/credits?api_key=d06ee9d17787be31829956793ca3e36b
# https://api.themoviedb.org/3/movie/44833/images?api_key=d06ee9d17787be31829956793ca3e36b


for movie in mycol.find():
    movie_id = movie["name"].split('_')[1].split('.')[0]
    actorUrl = BASE_ADDRESS + movie_id + "/credits" + API_KEY
    imageUrl = BASE_ADDRESS + movie_id + "/images" + API_KEY
    mycol.update_one({'_id': movie['_id']}, {'$set': {"actorUrl":actorUrl}})
    mycol.update_one({'_id': movie['_id']}, {'$set': {"imageUrl": imageUrl}})