from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os

import json
from PIL import Image
import requests
from io import BytesIO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)


def main():
    y_test = []
    x_test = []
    FILE_PATH = "/content/gdrive/MyDrive/TER/MoviesDataBase/movie_1202"
    IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"

    for movie in os.listdir(FILE_PATH):

        if movie.split(".")[1] != "json":
            continue
        movie_id = movie.split('_')[1].split('.')[0]
        fr = open(FILE_PATH + "/" + movie)

        movie_model = json.load(fr)
        fr.close()
        if movie_model['poster_path']:
            img_path = IMAGE_BASE_PATH + movie_model['poster_path']
            html = requests.get(img_path, verify=False)
            poster = Image.open(BytesIO(html.content))
            poster_img = poster.crop()

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
                    # print(np.shape(x_test))
                    # print(np.shape(x))
                    # exit(0)
                    x_test = np.concatenate((x_test, x))
                else:
                    x_test = x

    x_test = preprocess_input(x_test)

    model = ResNet50(weights='imagenet', include_top=False)

    features = model.predict(x_test)
    # print(np.shape(features))

    # print(len(y_test))
    features_compress = features.reshape(len(y_test), 7 * 7 * 2048)
    # print(np.shape(features_compress))
    # sim = cosine_similarity(features_compress)

    image_sample = Image.open("/content/gdrive/MyDrive/TER/Test/image2.jpg")
    imageS = image_sample.crop()
    thisImage = imageS.resize((224, 224))
    my_image = image.img_to_array(thisImage)
    my_x = np.expand_dims(my_image, axis=0)

    my_x = preprocess_input(my_x)

    my_features = model.predict(my_x)

    my_features_compress = my_features.reshape(1, 7 * 7 * 2048)

    new_features = np.append(features_compress, my_features_compress, axis=0)
    # print(np.shape(new_features))
    # exit(0)
    sim = cosine_similarity(new_features)
    # print("sim:", np.shape(sim))

    top = np.argsort(-sim[-1, :], axis=0)[1:3]

    recommend = [y_test[i] for i in top]
    print(recommend)
    # print(sim)


if __name__ == "__main__":
    main()