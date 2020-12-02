# coding=utf-8
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import string, os
from string import maketrans
import re
import numpy as np
from classification.lemmatization import lemmatization
import pickle
import time
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn import feature_extraction
from pymongo import MongoClient
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class Classification(object):
    path=' '
    host = '127.0.0.1'  # or localhost
    port = 27017
    client = MongoClient(host, port)
    # 创建数据库dialog
    db = client['allMovies']
    # 创建集合scene
    collection = db["Movie"]
    def __init__(self,path):
        self.path=path

    def Train(self):
        """
        Function to train data set
        """
        
        lem = lemmatization()
        #Get Mongo client
        # client = MongoClient()
        # db = client['IR']
        # collection = db['Movies']

        # host = '127.0.0.1'  # or localhost
        # port = 27017
        # client = MongoClient(host, port)
        # # 创建数据库dialog
        # db = client['allMovies']
        # # 创建集合scene
        # collection = db["Movie"]
        #print(collection.find_one({"content.genres.name":"Drama"}))

        #Path to folder to store trained data set
        path=self.path
        #Queries to get 500 horror, romance and crime movies
        qr1= self.collection.find({"content.genres.name":"Horror"}).limit(200)
        qr2= self.collection.find({"content.genres.name":"Romance"}).limit(200)
        qr3= self.collection.find({"content.genres.name":"Crime"}).limit(200)
        print (qr1)
        #Combine queries
        query_results=[]
        for rec in qr1:
            query_results.append(rec)
        for rec in qr2:
            query_results.append(rec)
        for rec in qr3:
            query_results.append(rec)
        print(query_results)
        #Dictionary to store the terms appearing in the genres
        dictionary = []

        #List to store category of each record
        categories = []
        
        training_data = []

        #Document ids of records to be trained
        doc_ids = []
        for movie in query_results:
            training_data.append(movie['content']['overview'])
            doc_ids.append(movie['_id'])
            
            for genre in movie['content']['genres']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   categories.append(genre['name'])
                   break
                
            #Convert to lower case and remove stop words from overview
            dict_rec = movie['content']['overview'].lower()
            #table = maketrans(string.punctuation, " ")
            for s in string.punctuation:
                dict_rec = dict_rec.replace(s, "")
            #dict_rec = str(dict_rec).translate(string.punctuation)
            dict_rec = lem.removeStopWords(dict_rec.split(" "))

            #Add to dictionary
            if dict_rec not in dictionary:
                dictionary.extend(dict_rec)
    
        dictionary = filter(None, list(set(dictionary)))

        #Store dictionary in a file
        joblib.dump(dictionary, path + "_Genre_Dictionary")
        
        #Store doc ids of trained data in a file
        myfile = open(r'doc_ids.pkl', 'wb')
        pickle.dump(doc_ids,myfile)
        myfile.close()

        #Initialize training models
        mod_1 = SVC(kernel='linear', C=1, gamma=1)
        mod_2 = LogisticRegression()
        mod_3 = GaussianNB()
        mod_4 = MultinomialNB()
        mod_5 = BernoulliNB()

        #Ensemble classifiers
        mod_6 = RandomForestClassifier(n_estimators=50)
        mod_7 = BaggingClassifier(mod_2, n_estimators=50)
        mod_8 = GradientBoostingClassifier(loss='deviance', n_estimators=100)

        mod_9 = VotingClassifier(
            estimators=[("SVM", mod_1), ("LR", mod_2), ("Gauss", mod_3), ("Multinom", mod_4), ("Bernoulli", mod_5),
                        ("RandomForest", mod_6), ("Bagging", mod_7), ("GB", mod_8)], voting='hard')
        mod_10 = VotingClassifier(estimators=[("SVM", mod_1), ("LR", mod_2), ("Multinom", mod_4),("Bernoulli", mod_5),("Bagging",mod_7)], voting='hard',weights=[1, 2, 3, 2,1])

        #Vectorizers for feature extraction
        vec_1 = feature_extraction.text.CountVectorizer(vocabulary=dictionary)
        vec_2 = feature_extraction.text.TfidfVectorizer(vocabulary=dictionary)
        
        vec_list = [vec_1, vec_2]

        #List of training models
        model_list = [mod_1, mod_2, mod_3, mod_4, mod_5, mod_6, mod_7, mod_8, mod_9, mod_10]
        
        models_used = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting", "Voting With Weights"]

        vec_used = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]

        print("Starting training. This might take a while...")

        #Start training
        for model in range(0, len(model_list)):
            for vec in range(0, len(vec_list)):
                mod = model_list[model]
                vector = vec_list[vec]
                X = vector.fit_transform(training_data).toarray()
                print(np.shape(X))
                print (np.shape(categories))
                mod.fit(X, categories)
                
                #Store in a file
                joblib.dump(mod, path + models_used[model] + "_" + vec_used[vec] + ".pkl")
                
                print(models_used[model] + " " + vec_used[vec]+" finished!")
                
        print("All Done!!")
        
    def Classify_Data(self):
        """
        Function to classify data from the database.
        Prints results of classification
        """

        lem = lemmatization()

        #Get Mongo Client
        # client = MongoClient()
        # db = client['IR']
        # collection = db['Movies']


        #Path to folder containing the training model files
        path=self.path

        #Get the list of doc ids trained
        trained_docs=[]

        #Mongo queries to retrieve Horror, Romance and Crime movies
        qr1 = self.collection.find({"content.genres.name":"Horror"})
        qr2 = self.collection.find({"content.genres.name":"Romance"})
        qr3 = self.collection.find({"content.genres.name":"Crime"})
        print ("111")
        print (qr1)

        myfile = open('doc_ids.pkl','rb')
        trained_docs = pickle.load(myfile)
        #Get 100 Horror, Romance and Crime movies each, which are not in the trained data set
        
        horr=[]
        i=0
        for rec in qr1:
            if rec['_id'] not in trained_docs:
               i=i+1
               horr.append(rec)
               
            if i>=333:
                break
        rom=[]
        i=0
        for rec in qr2:
            if rec['_id'] not in trained_docs:
               i=i+1
               rom.append(rec)
              
            if i>=333:
                break

        crime=[]
        i=0
        for rec in qr3:
            if rec['_id'] not in trained_docs:
               i=i+1
               crime.append(rec)
               
            if i>=334:
                break
                
        

        #Combine the query results
        query_results=[]
        for rec in horr:
            query_results.append(rec)
        for rec in rom:
            query_results.append(rec)
        for rec in crime:
            query_results.append(rec)
        print (query_results)
        #Data to be classified
        test_data = []

        #Genres of records to be classified 
        categories = []
        
        for movie in query_results:
            test_data.append(movie['content']['overview'])
            for genre in movie['content']['genres']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   categories.append(genre['name'])
                   break


        #Lists of training models and vectorizers
        models = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting","Voting With Weights"]

        vectorizers = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]

        #Load dictionary containing terms appearing in genres
        dictionary = joblib.load(path + "_Genre_Dictionary")
        
        vec_1 = feature_extraction.text.CountVectorizer(vocabulary=dictionary)
        vec_2 = feature_extraction.text.TfidfVectorizer(vocabulary=dictionary)
        vec_list = [vec_1, vec_2]

        #List to store the classification stats for each model
        stats = []
        #Generate results
        for i in range(0, len(models)):
            for j in range(0, len(vectorizers)):
                time0=time.clock()
                model = joblib.load(path + models[i] + "_" + vectorizers[j].replace('-', '') + ".pkl")
                vec = vec_list[j]
                Y = vec.fit_transform(test_data).toarray()
                predicted_genres = model.predict(Y)
                k = 0
                horror = 0
                romance = 0
                crime = 0

                #Keeps track of correct predictions
                y_correct = []

                #Keeps track of incorrect predictions
                y_predicted = []
                for pred in predicted_genres:
                    if (categories[k] == "Horror"):
                        if (pred == "Horror"):
                            horror += 1
                            y_predicted.append(0)
                        elif (pred == "Romance"):
                            y_predicted.append(1)
                        else:
                            y_predicted.append(2)
                        y_correct.append(0)
                    elif (categories[k] == "Romance"):
                        if (pred == "Romance"):
                            romance += 1
                            y_predicted.append(1)
                        elif (pred == "Horror"):
                            y_predicted.append(0)
                        else:
                            y_predicted.append(2)
                        y_correct.append(1)
                    elif (categories[k] == "Crime"):
                        if (pred == "Crime"):
                            crime += 1
                            y_predicted.append(2)
                        elif (pred == "Horror"):
                            y_predicted.append(0)
                        else:
                            y_predicted.append(1)
                        y_correct.append(2)
                    k = k + 1

                #Print results
                score = precision_recall_fscore_support(y_correct, y_predicted, average='weighted')
                #print("Number of records classified per second = %d" % (round((1000/(time.clock()-time0)),3)))
                print("________SCORES__________")
                print("MODEL      :  " + models[i])
                print("VECTORIZER :  " + vectorizers[j])
                print("Horror     :  %d/333" % (horror))
                print("Romance    :  %d/333" % (romance))
                print("Crime      :  %d/334" % (crime))
                print("Precision  :  %.5f" % (score[0]))
                print("Recall     :  %.5f" % (score[1]))
                print("F(1) Score :  %.5f" % ((score[1] * score[0] / (score[1] + score[0])) * 2))
                print("F(W) Score :  %.5f" % (score[2]))
                print("Accuracy   :  %.5f" % accuracy_score(y_correct, y_predicted))
                #print(confusion_matrix(y_correct, y_predicted))
                
                dic={}
                dic['model']=models[i].title()
                dic['vectorizer']=vectorizers[j][:-11]
                dic['horror']=str(horror)+'/'+'333'
                dic['romance']=str(romance)+'/'+'333'
                dic['crime']=str(crime)+'/'+'334'
                dic['precision']=round(score[0], 3)
                dic['Recall']=round(score[1], 3)
                dic['F(1) Score']=round(((score[1] * score[0] / (score[1] + score[0])) * 2), 3)
                dic['F(W) Score']=round(score[2], 3)
                dic['accuracy']=round(accuracy_score(y_correct, y_predicted), 3)
                stats.append(dic)
        #Store stats in file        
        joblib.dump(stats, path + "classification_results.txt")

        print("Done")
        return stats
    

    def Classify_Text(self,overview):
        """
        Function takes in the overview of a movie as input from the user and classifies the text
        """

        #convert text to lower case 
        overview = overview.lower()
        
        path=self.path        

        #start time
        time0 = time.clock()

        #Use ensemble classifier - voting with weights
        model = joblib.load(path + "MULTINOMIAL NB_TFIDF VECTORIZER" + ".pkl")
        dictionary = joblib.load(path + "_Genre_Dictionary")
        vec = feature_extraction.text.CountVectorizer(vocabulary=dictionary)
        print(vec)
        Y = vec.fit_transform([overview]).toarray()
        print (Counter(Y[0]))
        predicted_genre = model.predict(Y)
        print (predicted_genre)

        
        #Return predicted genre and time taken for classification
        return predicted_genre, str(round(time.clock() - time0, 3)) + " seconds"


    def get_classification_results(self):
        """
        This functions returns a data structure containing the results of classification
        """
        try:
            path=self.path
            print(path + "classification_results.txt")
            results = joblib.load(path + "classification_results.txt")
            print(results)
            return results
        
        #Call Classify_Data() if results are not found
        except EOFError as eoferror:
            print ("Classification results not found. Generating results...")
            return self.Classify_Data()
        except IOError as ioerror:
            print ("Classification results not found. Generating results...")
            return self.Classify_Data()



# path='/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/frontend/static/frontend/text/'
# c = Classification(path)
# c.Train()
# c.Classify_Data()
# c.Classify_Text("An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.")
# print c.get_classification_results()
