import glob
import json
import ast
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
from numpy import unicode

filenames=[]
for filename in glob.glob('../*.txt'):
    filenames.append(filename)
count=0
words = set(nltk.corpus.words.words())
overviews=[]
ids=[]
iddict={}
iddictinv={}
overdict={}

porter=PorterStemmer()
for f in filenames:
    #if count==2:
        #break
    print(count)
    file=open(f,"r")
    doc=ast.literal_eval(file.read())
    #print(doc['id'],doc['overview'])
    
    x=doc['overview'].lower()
    if x:
    	
        sent=""
        ids.append(doc['id'])
        iddict[doc['id']]=count
        iddictinv[count]=doc['id']
        overdict[doc['id']]=x
        y=x.split()
    
        for i in y:
        #i=i.lower()
            if i not in words:
              continue
            if i in stopwords.words('english'):
                continue
            else:
            #j=i
                sent=sent+i+' '
    #overviews.append(sent)

    #Extract noun phrases 
        blob = TextBlob(sent)
    #print(blob.noun_phrases)
        sent1=""
        z=blob.noun_phrases
        for x in z:
        #x=unidecode(x)
            x=x.encode('utf-8')
            sent1=sent1+x+" "
        
    #print(type(sent1))
        overviews.append(sent1)

    #for i in y
    #overviews.append(x)
    #overviews[doc['id']]=x
    count=count+1
print("done")
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(overviews)
x=(tfidf_matrix * tfidf_matrix.T).A
i=0
j={}
for v in x:
    j[(iddict.keys())[i]]=v
    i=i+1
m={}
i=0
for k in j.keys():
    if i==51:
        break
    else:
        i=i+1
    #i=i+1
        for n in j.keys():
           if n!=k:
                print(k,n)
                m[k,n]=cosine_similarity(j[k].reshape(1,-1),j[n].reshape(1,-1))

    
print('DONE')
pickle.dump(overviews,open( "overviews.p", "wb" ))
pickle.dump(ids,open( "ids.p", "wb" ))
pickle.dump(iddict,open( "iddict.p", "wb" ))
pickle.dump(overdict,open( "overdict.p", "wb" ))
pickle.dump(iddictinv,open( "iddictinv.p", "wb" ))

pickle.dump( m, open( "cosinesimilarity.p", "wb" ) )