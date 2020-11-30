import sys
import os
import fnmatch
import urllib
import json
#from datetime import datetime, timedelta
from datetime import timedelta
from indexing.MovieDataIndexing import Indexing

API_KEY = "857995276b571b316947f8eda9394c26"

def get_file_path(directory, filename):
    return os.path.join(directory, filename)

def get_current_record_count(write_directory):
    all_files = os.listdir(write_directory) # dir is your directory path
    number_files = len(fnmatch.filter(all_files, '*.txt'))
    return number_files


def store_movies(jsonRecords, write_directory):
        current_records = get_current_record_count(write_directory)
        counter = current_records
        for item in jsonRecords['results']:
            counter += 1
             ## Cleaning data
            item['revenue'] = 0
            item['tagline'] = None
            item['production_companies'] = None
            item['revenue'] = 0
            item['runtime'] = 0
            item['genres'] = None
            stor = json.dumps(item)
            stor = stor.replace("id","imdb_id")
            stor = stor.replace("false", "False")
            stor = stor.replace("true", "True")
            stor = stor.replace("null", "None")
            # Done cleaning
            name = get_file_path(write_directory, str(counter)+".txt")
            with open(name, 'w') as outfile:
                outfile.write(stor)
        total_records_stored = counter - current_records

        return current_records, total_records_stored


def get_movie(start_date, write_directory):
    end_date = start_date + timedelta(days=1)
    url = "https://api.themoviedb.org/3/discover/movie?api_key="+API_KEY+"&"+\
          "primary_release_date.gte="+start_date.strftime("%Y-%m-%d")+\
          "&primary_release_date.lte="+end_date.strftime("%Y-%m-%d")+\
          "&page=1"
    x = urllib.urlopen(url).read()
    y = json.loads(x.decode('utf-8'))
    return store_movies(y,write_directory)


def crawl_and_update(start_date, write_directory, index_file):
    current, to_index = get_movie(start_date, write_directory)
    obj = Indexing(index_file)
    for i in range(current+1, current+to_index):
        file_path = get_file_path(write_directory,str(i)+".txt")
        obj.write_single_index(file_path)

    return to_index

