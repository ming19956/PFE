from django.shortcuts import render
from .forms import SearchForm, ClassifyForm
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
from sklearn.externals import joblib
from django.templatetags.static import static

INDEX_FILE = '/Users/liujiazhen/Documents/2020-2021/PFE/PFE3.7/PFE-pfe/Index_tmp'
WRITE_FILE = '/Users/liujiazhen/Documents/2020-2021/PFE/PFE3.7/PFE-pfe/Trial_2'
CLASSIFICATION_PATH = '/Users/liujiazhen/Documents/2020-2021/PFE/PFE/PFE/information-retrival-search-engine/informationRetrival/classification'

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
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            query = form.cleaned_data['search_text']
            rating = request.GET.get("rating")
            year = request.GET.get("year")

            genre_list = request.GET.getlist('multi_genre')


            query = query.replace('+', ' AND ').replace('-', ' NOT ')

            filter_q = None
            # TODO: Change Directory here
            ix = i.open_dir(INDEX_FILE)
            start_time = time.time()
            if query is not None and query != u"":
                parser = MultifieldParser(search_field, schema=ix.schema)
                if year is not None:
                    date_q = QRY.DateRange("release_date", datetime.strptime(year.split(",")[0], "%Y"), datetime.strptime(year.split(",")[1], "%Y"))
                    rating_q = QRY.NumericRange("vote_average",int(rating.split(",")[0]), int(rating.split(",")[1]))

                    if len(genre_list)>0:
                        genres_q=QRY.Or([QRY.Term(u"genres",unicode(x.lower())) for x in genre_list])
                        combi_q = QRY.And([rating_q, genres_q])
                        filter_q = QRY.Require(date_q, combi_q)
                    else:
                        filter_q = QRY.Require(date_q, rating_q)


                    print(filter_q)

                else:
                    year = "1900,2020"
                    rating = "-1,10"

                try:
                    qry = parser.parse(query)

                except:
                    qry = None
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Query is null!", 'form':form})
                if qry is not None:
                    searcher = ix.searcher(weighting=scoring.TF_IDF())
                    corrected = searcher.correct_query(qry, query)
                    if corrected.query != qry:
                        return render(request, 'frontend/index.html', {'search_field': search_field, 'correction': True, 'suggested': corrected.string, 'form': form})
                    print(qry,filter_q)
                    hits = searcher.search(qry, filter=filter_q, limit=None)
                    print(hits)
                    elapsed_time = time.time() - start_time
                    elapsed_time = "{0:.3f}".format(elapsed_time)
                    return render(request, 'frontend/index.html', {'search_field': search_field, 'search_text': form.cleaned_data['search_text'],
                                                                   'error': False, 'hits': hits, 'form':form, 'elapsed': elapsed_time,
                                                                   'number': len(hits), 'year': year, 'rating': rating, 'multi_genre': genre_list})
                else:
                    return render(request, 'frontend/index.html', {'error': True, 'message':"Sorry couldn't parse", 'form':form})
            else:
                return render(request, 'frontend/index.html', {'error': True, 'message':'oops', 'form':form})
        else:
            form = SearchForm()
            return render(request, 'frontend/index.html', {'form': form})


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
        print (len(hits))
        if (len(hits)==0):
        # send new records directory to the indexing function to add them to the index
            total_records = crawl_and_update(date_now, WRITE_FILE, INDEX_FILE)
        else:
            total_records = "Already up-to-date"
        return render(request, 'frontend/crawl.html', {'total_records': total_records, 'form': form})
