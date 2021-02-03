#import cv2
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import os
import sys
import json
from PIL import Image
# import Image
import requests
from io import BytesIO
import urllib3
import h5py

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# y_test = []

# 計算相似矩陣
def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def saveVector(vector): ## don't use, just use it in colab to get the vector
    save_file = h5py.File('../test.h5', 'w')
    save_file.create_dataset('test', data=vector)
    save_file.close()

def readvector():
    open_file = h5py.File('/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/vgg16_p/test.h5', 'r')
    vector = open_file['test'][:]
    open_file.close()
    return vector

def getTitleCheck_VGG():
    a = np.load('/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/vgg16_p/title.npy', allow_pickle= True)
    return a.item()

def compare():
    # y_test = []
    model = VGG16(weights='imagenet', include_top=False)
    # 取样本
    image_sample = Image.open("/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/frontend/static/frontend/images/temp.jpg")
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
    y_test = getTitleCheck_VGG()
    recommend = [y_test[i] for i in top]
    print(recommend)
    # print(sim)

def compare_melanger():
    # y_test = []
    model = VGG16(weights='imagenet', include_top=False)
    # 取样本
    image_sample = Image.open("/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/frontend/static/frontend/images/temp.jpg") # 此处添加修改地址
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
    return sim



def main():
    # 自 images 目錄找出所有 JPEG 檔案

    y_test = []
    x_test = []
    # x_test_final = []
    # FILE_PATH = "/Users/panda/Desktop/movie_1202"
    FILE_PATH = "/Users/panda/Downloads/archive/movies/movies"


    IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
    flag = 0

    # read file which is in the id_list
    open_file = h5py.File('./id_list.h5', 'r')
    id = open_file['id'][:]
    open_file.close()
    tmp = []
    for i in range(len(id)):
        tmp.append(int(id[i].decode('UTF-8')))
        # print(tmp)

    for movie in os.listdir(FILE_PATH):
        # if flag < 50:
            # flag += 1
            # if flag == 245 or flag == 246 or flag == 247 or flag == 248:
            #     print(movie)
            # else:
            #     continue
            if movie.split(".")[1] != "json":
                continue
            movie_id = int(movie.split('_')[1].split('.')[0])


            if movie_id in tmp:
                # print(movie_id)
                # open file
                fr = open(FILE_PATH + "/" + movie)
                # print(movie)
                # print(movie_id)
                movie_model = json.load(fr)
                fr.close()
                if movie_model['poster_path']:
                    img_path = IMAGE_BASE_PATH + movie_model['poster_path']
                    html = requests.get(img_path, verify=False)
                    poster = Image.open(BytesIO(html.content))
                    poster_img = poster.crop()
                    # poster = html.content
                    # imgByteArr = BytesIO()
                    # poster.save(imgByteArr, format=poster.format)
                    # poster = imgByteArr.getvalue()

                    # poster_img.show()
                    # img = poster_img.resize((224, 224))
                    # img.show()
                    # exit(1)
                    if poster:
                        # img = image.load_img(poster_img, target_size=(224, 224))
                        img = poster_img.resize((224, 224))
                        # img.show()
                        y_test.append(movie_id)
                        x = image.img_to_array(img)
                        # print(movie_id)
                        # print(x[:,:,0])
                        # print(np.shape(x[:,:,0]))
                        # exit(0)
                        if np.shape(x)[2] == 1:
                            x = np.stack((x[:, :, 0],) * 3, axis=-1)
                        x = np.expand_dims(x, axis=0)

                        if len(x_test) > 0:
                            # print(1)
                            # print(np.shape(x_test))
                            # print(np.shape(x))
                            # exit(0)
                            x_test = np.concatenate((x_test, x))
                        else:
                            # print(2)
                            x_test = x
                # flag = flag + 1


        # else:
        #     if len(x_test_final) > 0:
        #         # print(np.shape(x_test))
        #         # print(np.shape(x))
        #         # exit(0)
        #         #x_test = preprocess_input(x_test)
        #         x_test_final = np.concatenate((x_test_final, x_test))
        #     else:
        #         # x_test = preprocess_input(x_test)
        #         x_test_final = x_test
        #     x_test = []
        #     flag = 0


    # x_test_final = np.concatenate((x_test_final, x_test))

    # 轉成 VGG 的 input 格式
    # print(x_test)
    # print(type(x_test))
    # print(np.shape(x_test))
    x_test = preprocess_input(x_test)
    # print(np.shape(x_test_final))

    np.save("title.npy", y_test)

    # include_top=False，表示會載入 VGG16 的模型，不包括加在最後3層的卷積層，通常是取得 Features (1,7,7,512)
    model = VGG16(weights='imagenet', include_top=False)

    # 萃取特徵
    features = model.predict(x_test)
    # print(np.shape(features))
    # 計算相似矩陣
    features_compress = features.reshape(len(y_test), 7 * 7 * 512)
    # print(np.shape(features_compress))
    # sim = cosine_similarity(features_compress)
    saveVector(features_compress)

    compare()


    # # 取样本
    # image_sample = Image.open("/Users/panda/Desktop/test_image/test.jpg")
    # imageS = image_sample.crop()
    # thisImage = imageS.resize((224, 224))
    # my_image = image.img_to_array(thisImage)
    # my_x = np.expand_dims(my_image, axis=0)
    #
    # my_x = preprocess_input(my_x)
    #
    # my_features = model.predict(my_x)
    #
    # my_features_compress = my_features.reshape(1, 7 * 7 * 512)
    #
    # # features_compress.append(my_features_compress)
    #
    # # print(np.shape(features_compress))
    # # print(np.shape(my_features_compress))
    # new_features = np.append(features_compress, my_features_compress, axis=0)
    # # print(np.shape(new_features))
    # # exit(0)
    # sim = cosine_similarity(new_features)
    # # print("sim:", np.shape(sim))
    #
    #
    # # # 依命令行參數，取1個樣本測試測試
    # # inputNo = int(sys.argv[1])  # tiger, np.random.randint(0,len(y_test),1)[0]
    # # sample = y_test[inputNo]
    # # print(sample)
    # top = np.argsort(-sim[-1,:], axis=0)[1:3]
    #
    # # 取得最相似的前2名序號
    # recommend = [y_test[i] for i in top]
    # print(recommend)
    # #print(sim)




# if __name__ == "__main__":
#     main()
print(getTitleCheck_VGG())