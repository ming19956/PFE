from django.shortcuts import render
from .forms import SearchForm, ClassifyForm, UploadFileForm
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh import index as i
from whoosh import scoring
import whoosh.query as QRY
import time
import pandas as pd
import os
from datetime import datetime
from indexing.crawl import crawl_and_update
from classification.classify import Classification
from numpy import unicode
from .vgg16_p import compare
from  classification.bert import todo
import joblib
from django.templatetags.static import static

INDEX_FILE = '/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/Index_tmp'
WRITE_FILE = '/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/Trial_2'
CLASSIFICATION_PATH = '/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/information-retrival-search-engine/informationRetrival/frontend/static/frontend/text/'

HITS = [1,2,3]

def show(request):
    if request.method == 'POST':
        overview = request.POST.get('overview')
        title = request.POST.get('title')
        poster_path = request.POST.get('poster_path')
        id = request.POST.get('imdb_id')
        print (id)
        ix = i.open_dir(INDEX_FILE)
        searcher = ix.searcher()
        docnum = searcher.document_number(imdb_id=id)
        recoms = searcher.more_like(docnum,'overview')
        return render(request, 'frontend/show.html', {'overview': overview, 'title': title, 'poster_path': poster_path, 'recommendations': recoms})

def index(request):
    if request.method == 'POST':


        search_list = request.POST.getlist("search")
        query = request.POST.get("search_text")
        file_obj = request.FILES.get('uploadPicture')
        print(file_obj)
        print(query)
        res = []
        start_time = time.time()
        if file_obj is not None :
            with open('frontend/static/frontend/images/temp.jpg', 'wb+') as destination:
                destination.write(file_obj.read())
            res = res+compare()

        if query is not None and query is not '':
            search_field = search_list
            query = query.replace('+', ' AND ').replace('-', ' NOT ')

            res = res+todo(query)
            print(res)

        if len(res) > 0  :

            year = "1900,2020"
            rating = "0,10"
            ix = i.open_dir(INDEX_FILE)
            searcher = ix.searcher(weighting=scoring.TF_IDF())
            res_q = QRY.Or([QRY.Term(u"movie_id", unicode(x)) for x in res])
            print(res_q)
            hits= searcher.search(res_q, filter=None, limit=None)
            elapsed_time = time.time() - start_time
            return render(request, 'frontend/index.html',
                          {'search': search_list, 'error': False, 'hits': hits, 'search_text': query,
                           'elapsed': elapsed_time, 'number': len(hits), 'year': year, 'rating': rating, 'results':res})

    else:
        return render(request, 'frontend/index.html', {'search_text': ""})


def filter(request):
    res = request.GET.getlist("result")
    print(res)
    res_q = QRY.Or([QRY.Term(u"movie_id", unicode(x)) for x in res])
    rating = request.GET.get("rating")
    year = request.GET.get("year")
    query = request.GET.get("search_text")
    genre_list = request.GET.getlist('multi_genre')
    date_q = QRY.DateRange("release_date", datetime.strptime(year.split(",")[0], "%Y"),datetime.strptime(year.split(",")[1], "%Y"))
    rating_q = QRY.NumericRange("vote_average",int(rating.split(",")[0]), int(rating.split(",")[1]))
    filter_q = QRY.And([date_q, rating_q])
    filter_q = QRY.And([filter_q,res_q])
    if len(genre_list) > 0:
        genres_q=QRY.Or([QRY.Term(u"genres",unicode(x.lower())) for x in genre_list])
        filter_q = QRY.And([filter_q, genres_q])

    ix = i.open_dir(INDEX_FILE)
    searcher = ix.searcher(weighting=scoring.TF_IDF())
    print(filter_q)
    hits= searcher.search(filter_q, filter=None, limit=None)
    return render(request, 'frontend/index.html',
                  { 'error': False, 'hits': hits, 'search_text': query,
                    'number': len(hits), 'year': year, 'rating': rating})


    #         rating = request.GET.get("rating")
    #         year = request.GET.get("year")
    #         genre_list = request.GET.getlist('multi_genre')
    #         filter_q = None
    #         # TODO: Change Directory here
    #         ix = i.open_dir(INDEX_FILE)
    #         start_time = time.time()
    #         if query is not None and query != u"":
    #             parser = MultifieldParser(search_field, schema=ix.schema)
    #             if year is not None:
    #                 date_q = QRY.DateRange("release_date", datetime.strptime(year.split(",")[0], "%Y"), datetime.strptime(year.split(",")[1], "%Y"))
    #                 rating_q = QRY.NumericRange("vote_average",int(rating.split(",")[0]), int(rating.split(",")[1]))
    #
    #                 if len(genre_list)>0:
    #                     genres_q=QRY.Or([QRY.Term(u"genres",unicode(x.lower())) for x in genre_list])
    #                     combi_q = QRY.And([rating_q, genres_q])
    #                     filter_q = QRY.Require(date_q, combi_q)
    #                 else:
    #                     filter_q = QRY.Require(date_q, rating_q)
    #
    #
    #             else:
    #                 year = "1900,2020"
    #                 rating = "0,10"
    #
    #             try:
    #                 qry = parser.parse(query)
    #
    #             except:
    #                 qry = None
    #                 return render(request, 'frontend/index.html', {'error': True, 'message':"Query is null!"})
    #             if qry is not None:
    #                 searcher = ix.searcher(weighting=scoring.TF_IDF())
    #                 corrected = searcher.correct_query(qry, query)
    #                 if corrected.query != qry:
    #                     return render(request, 'frontend/index.html', {'search_field': search_field, 'correction': True, 'suggested': corrected.string, 'search_text':query})
    #                 print(qry,filter_q)
    #                 hits = searcher.search(qry, filter=filter_q, limit=None)
    #                 print(hits)
    #                 elapsed_time = time.time() - start_time
    #                 elapsed_time = "{0:.3f}".format(elapsed_time)
    #                 print(query,search_list)
    #                 return render(request, 'frontend/index.html', {'search': search_list,'error': False, 'hits': hits, 'search_text': query, 'elapsed': elapsed_time,
    #                                                                'number': len(hits), 'year': year, 'rating': rating})
    #             else:
    #                 return render(request, 'frontend/index.html', {'error': True, 'message':"Sorry couldn't parse", 'search_text':query})
    #         else:
    #             return render(request, 'frontend/index.html', {'error': True, 'message':'oops', 'search_text':query})
    #     else:
    #         return render(request, 'frontend/index.html', {'search_text':""})
    # else:
    #     return render(request, 'frontend/index.html', {'search_text': ""})
    #

def classification(request):
    results_dict = Classification(CLASSIFICATION_PATH).get_classification_results()
    results = pd.DataFrame(results_dict)
    for column in ['romance','crime','horror']:
        results[column] = results[column].apply(lambda x: str((int(x.split('/')[0]) * 100)/int(x.split('/')[1]))+" %")

    results.columns = ['F(1) Score', 'F(W) Score', 'Recall', 'Accuracy', 'Crime', 'Horror', 'Model', 'Precision', 'Romance','Vectorizer']
    results = results[['Model','Vectorizer', 'Crime', 'Horror', 'Romance', 'F(1) Score', 'F(W) Score', 'Recall', 'Accuracy', 'Precision']]
    results = results.to_html

    if request.method == "POST":
        form = ClassifyForm(request.POST)
        if form.is_valid():
            plot = form.cleaned_data['classify_plot']
            genre, time = Classification(CLASSIFICATION_PATH).Classify_Text(plot)
            return render(request, 'frontend/classify.html', {'results': results, 'form': form, 'genre': genre[0], 'time': time})
        else:
            return render(request, 'frontend/classify.html', {'results': results, 'form': form})
    else:
        form = ClassifyForm()
        return render(request, 'frontend/classify.html', {'results': results, 'form': form})


def crawl(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        date_now = datetime.now()
        search_field = request.GET.get('search_field')
        query = request.GET.get('search_text')
        ix = i.open_dir(INDEX_FILE)
        parser = QueryParser("release_date", schema=ix.schema)
        qry = parser.parse(date_now.strftime("%Y-%m-%d"))
        searcher = ix.searcher()
        hits = searcher.search(qry, limit=1)
        if (len(hits)==0):
        # send new records directory to the indexing function to add them to the index
            total_records = crawl_and_update(date_now, WRITE_FILE, INDEX_FILE)
        else:
            total_records = "Already up-to-date"
        return render(request, 'frontend/crawl.html', {'total_records': total_records, 'form': form})






def handleImg(request):
    year = "1900,2020"
    rating = "0,10"

    start_time = time.time()
    form = UploadFileForm(request.POST, request.FILES)
    print(request.FILES)

    file_obj = request.FILES.get('upload_picture')
    with open('frontend/static/frontend/images/temp.jpg', 'wb+') as destination:
        destination.write(file_obj.read())
    res = compare()

    ix = i.open_dir(INDEX_FILE)
    searcher = ix.searcher(weighting=scoring.TF_IDF())

    res_q = QRY.Or([QRY.Term(u"movie_id", unicode(x.lower())) for x in res])

    # parser = MultifieldParser(search_field, schema=ix.schema)


    hits = searcher.search(res_q, filter=None, limit=None)
    elapsed_time = time.time() - start_time
    return


