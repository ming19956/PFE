from pymongo import MongoClient
from collections import Counter
import sys
import importlib
import pandas as pd
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
importlib.reload(sys)



class bert(object):
    path = ' '
    host = '127.0.0.1'  # or localhost
    port = 27017
    client = MongoClient(host, port)
    # 创建数据库dialog
    db = client['allMovies']
    # 创建集合scene
    collection = db["Movie"]
    label = []
    over = []
    def __init__(self):
        pass

    def getInfo(self):
        # qr1 = self.collection.find({"content.overview"}).limit(200)
        # qr2 = self.collection.find({"name"}).limit(200)
        # dataset = {}
        # for i,j in [qr1,qr2]:
        #     dataset[j] = i
        # return dataset

        data = pd.DataFrame(list(self.collection.find()))

        # 选择需要显示的字段
        data = data[['content', 'name']]
        for i in range(len(data['content'])):
            self.label.append(data['name'][i])
            if len(data['content'][i]['overview']) < 2:
                self.over.append("Nothing")
            else:
                self.over.append(data['content'][i]['overview'])
        return self.label, self.over

a = bert()
label, over = a.getInfo()
bc = BertClient(check_length=False)
matrix = bc.encode(over)
print(type(matrix))