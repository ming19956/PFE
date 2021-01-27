from pymongo import MongoClient
from collections import Counter
import sys
import importlib
import pandas as pd
from bert_serving.client import BertClient
import h5py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
importlib.reload(sys)

def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def getVector():
    open_file = h5py.File(
        '/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/classification/vector.h5',
        'r')
    vector = open_file['vector'][:]
    open_file.close()
    return vector

def getMain_info():
    a = np.load('/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/classification/main_info.npy', allow_pickle= True)
    return a.item()

def getTitleCheck_BERT():
    a = np.load('/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/classification/title_check.npy', allow_pickle= True)
    return a.item()

def creatSearchVector(text):
    a = bert()
    # label, over = a.getInfo()
    # bc = BertClient(check_length=False)
    over = text
    matrix = a.getSearchVector(over)
    return matrix

def getMostSimilar(vectorAll, vectorSearch, search_type):
    vectorCos = np.append(vectorAll, vectorSearch, axis = 0)
    res = cosine_similarity(vectorCos)
    print(-res[-1,:])
    top = np.argsort(-res[-1, :], axis=0)[1:30]
    y = getTitleCheck_BERT()
    z = getMain_info()
    print(top)
    recommend = []
    if search_type == 1:
        for i in top:
            if z[y[i-1]] is 'title':
                recommend.append(y[i-1])
    elif search_type == 2:
        for i in top:
            if z[y[i-1]] is 'content':
                recommend.append(y[i-1])
    else:
        recommend = [y[i-1] for i in top]
    return recommend

def getMostSimilar_BERT(vectorAll, vectorSearch, search_type):
    vectorCos = np.append(vectorAll, vectorSearch, axis = 0)
    res = cosine_similarity(vectorCos)
    return res

## 直接调用这个函数，可以直接返回id
## just use this
## search_type :: 1 -> title | 2 -> overview | 3 -> title + overview
def todo(text, search_type):
    vectorSearch = creatSearchVector(text)
    vectorAll = getVector()
    res = getMostSimilar(vectorAll, vectorSearch, search_type)
    return res

def todo_melanger(text, search_type):
    vectorSearch = creatSearchVector(text)
    vectorAll = getVector()
    res = getMostSimilar_BERT(vectorAll, vectorSearch, search_type)
    return res  # similarity




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
    vector = []
    bc = BertClient(port = 8190, port_out= 8191, check_length=False)
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

    def saveVector(self): ## don't use, just use it in colab to get the vector
        save_file = h5py.File('../test.h5', 'w')
        save_file.create_dataset('test', self.vector)
        save_file.close()

    def readvector(self):
        open_file = h5py.File('/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/classification/vector.h5', 'r')
        self.vector = open_file['vector'][:]
        open_file.close()
        return self.vector

    def getSearchVector(self, search_text):
        tmp = []
        tmp.append(search_text)
        matrix = self.bc.encode(tmp)
        return matrix



a = bert()
#label, over = a.getInfo()
#bc = BertClient(check_length=False)
over = 'Avatar'
matrix = a.getSearchVector(over)
all_v = getVector()
print(np.shape(all_v))
print(np.shape(matrix))
b = getMostSimilar(all_v, matrix)
print(b)