def getmovie(query):
    import urllib.request
    import json
    url="https://api.themoviedb.org/3/search/movie?api_key=4413e4bd6b1b3f708ae7847af1b27379&language=en-US&query="+query+"&page=1&include_adult=false"
    x=urllib.request.urlopen(url).read()
    y=json.loads(x.decode('utf-8'))
    return y['results']
x=getmovie("Bourne")