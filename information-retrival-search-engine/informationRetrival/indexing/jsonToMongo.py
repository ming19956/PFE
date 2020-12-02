# coding=utf-8
from pymongo import MongoClient
import json
import os

BASE_PATH="/Users/panda/Desktop/movie/information-retrival-search-engine/trial"



host = '127.0.0.1' # or localhost
port = 27017
    # 创建mongodb客户端
client = MongoClient(host, port)
    # 创建数据库dialog
db = client.allMovies
    # 创建集合scene
collection = db.Movie


# 写入数据库
def write_database(path, file):
    with open(path + "/" + file, 'r') as f:
        # 转换为dict
        json_data = json.load(f)
    data = {
        "name": file,
        "content": json_data
    }
    try:
        myquery = {"name": file}  # 查询条件
        collection.update(myquery, data, upsert=True)  # upsert=True不存在则插入，存在则更新
        # self.collection.insert(data)
        print('Insert successfully')
    except Exception as e:
        print(e)


all_file = os.listdir(BASE_PATH)
for file in all_file:
    write_database(BASE_PATH, file)