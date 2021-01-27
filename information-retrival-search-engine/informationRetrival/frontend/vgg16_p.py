from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import os
import sys
import json
from PIL import Image
import requests
from io import BytesIO
import urllib3
import h5py

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def readvector():
    open_file = h5py.File('/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/test.h5', 'r')
    vector = open_file['test'][:]
    open_file.close()
    return vector

def getTitleCheck():
    a = np.load('/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/vgg16/title.npy', allow_pickle= True)
    return a
def compare():
    # y_test = []
    model = VGG16(weights='imagenet', include_top=False)
    # 取样本
    image_sample = Image.open("frontend/static/frontend/images/temp.jpg")
    imageS = image_sample.crop()
    thisImage = imageS.resize((224, 224))
    my_image = image.img_to_array(thisImage)
    my_x = np.expand_dims(my_image, axis=0)

    my_x = preprocess_input(my_x)

    my_features = model.predict(my_x)

    my_features_compress = my_features.reshape(1, 7 * 7 * 512)

    # features_compress.append(my_features_compress)
    features_compress = readvector()

    # print(np.shape(features_compress))
    # print(np.shape(my_features_compress))
    new_features = np.append(features_compress, my_features_compress, axis=0)
    # print(np.shape(new_features))
    # exit(0)
    sim = cosine_similarity(new_features)
    # print("sim:", np.shape(sim))

    # # 依命令行參數，取1個樣本測試測試
    # inputNo = int(sys.argv[1])  # tiger, np.random.randint(0,len(y_test),1)[0]
    # sample = y_test[inputNo]
    # print(sample)
    top = np.argsort(-sim[-1, :], axis=0)[1:3]

    # 取得最相似的前2名序號
    y_test = getTitleCheck()
    recommend = [y_test[i] for i in top]
    print(recommend)
    return recommend