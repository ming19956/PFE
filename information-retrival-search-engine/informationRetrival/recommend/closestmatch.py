import pickle
encoding="utf8"

overviews=pickle.load(open( "pickle_files/overviews.p", "rb"))
ids=pickle.load(open( "pickle_files/ids.p", "rb" ))
overdict=pickle.load(open( "pickle_files/overdict.p", "rb" )) #, encoding="latin-1")
iddict=pickle.load(open( "pickle_files/iddict.p", "rb" ))
iddictinv=pickle.load(open( "pickle_files/iddictinv.p", "rb" ))

cosinesim=pickle.load(open( "pickle_files/cosinesimilarity.p", "rb" )) #,encoding="latin-1")

# Function takes input as id
def findsim(i):
    
    sim=0
    maxsim=[]
    for j in iddict.keys():
        if j!=i:
            if cosinesim[(i,j)]>sim:
                sim=cosinesim[(i,j)]
                
                maxsim.append(j)
    maxsim=sorted(maxsim,reverse=True)
    #returns top 5 matching results
    return maxsim[:5]


#returning only values for iddict[:50]
x=0

for i in iddict.keys():
    if x<=50:
        print(i,findsim(i))
        x=x+1
        