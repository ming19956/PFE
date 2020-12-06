
import os
import argparse
from indexing.MovieData import MovieData
from whoosh.fields import Schema, TEXT, ID, STORED, DATETIME, NUMERIC, BOOLEAN
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
from numpy import unicode

LIST_OF_FIELDS = ["overview", "tagline", "title", "runtime", "poster_path", "genres",
                "production_companies", "release_date", "imdb_id", "popularity", "revenue", "vote_average", "adult"]


class Indexing:

    def __init__(self, index_folder, create=False):
        if not os.path.exists(index_folder):
            os.mkdir(index_folder)
        # if creating a new index
        if create:
            self.ix = index.create_in(index_folder, self.get_schema())
        # if adding to existing index
        else:
            self.ix = index.open_dir(index_folder)

    @staticmethod
    def get_schema():
        """
        :return: Current Schema
        """
        return Schema(overview=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
                      tagline=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
                      title=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
                      production_companies=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
                      genres=TEXT(analyzer=StemmingAnalyzer(), spelling=True, stored=True),
                      runtime=STORED,
                      poster_path=STORED,
                      imdb_id=ID(stored=True),
                      popularity=NUMERIC(float, bits=64, stored=True),
                      revenue=NUMERIC(float, bits=64, stored=True),
                      vote_average=NUMERIC(float, bits=64, stored=True),
                      adult=BOOLEAN(stored=True),
                      release_date=DATETIME(stored=True)
                      )

    @staticmethod
    def index_doc(file_path, list_of_fields):
        """

        :param file_path: path to Document
        :param list_of_fields: list of fields required to extract from document
        :return: dictionary of data
        """
        current_doc = MovieData(file_path)
        current_data = dict()
        for key in list_of_fields:
            item = current_doc.get(key)

            if isinstance(item, str):
                item = unicode(item, errors='ignore')
            value = u""
            if isinstance(item, list):
                for temp in item:
                    value += unicode(temp['name'], errors='ignore')+" "
            else:
                value = item
            if key == "release_date" and item == "":
                value = u'2100-10-10'
            if value == '':
                value = u''
            current_data[key] = value

        return current_data

    def write_index(self, directory_path, list_of_fields, optimise=True, merge=True):
        """
        Add multiple documents to the index. Typically for creating indexes initially
        :param directory_path: Directory to the folder containing all the documents
        :param list_of_fields: Keywords corresponding to mapping for schema to document items
        :param optimise: if index exists, whoosh creates a new segment and on search both segments are looked.
                        if it costs search speed, optimise=True helps unify all segments into 1 segment
        :param merge: Whoosh automatically merges smalls segments by default during commit, thus True
        :return:
        """

        # Open index writer
        writer = self.ix.writer()

        # counter to count every document
        counter = 0

        # For each file in the directory
        for filename in os.listdir(directory_path):
            if ".txt" not in filename:
                continue
            # combining the path names
            file_path = os.path.join(directory_path, filename)
            # get file data
            data = self.index_doc(file_path, list_of_fields)
            try:
                # Add file data to index writer. Unicode conversion is required by Whoosh.
                writer.add_document(overview=data['overview'], tagline=data['tagline'], title=data['title'], production_companies=data['production_companies'],
                                    genres=data['genres'], runtime=data['runtime'], poster_path=data['poster_path'], imdb_id=data['imdb_id'], popularity=data['popularity'],
                                    revenue=data['revenue'], vote_average=data['vote_average'], adult=data['adult'], release_date=data['release_date'])
            except Exception as err:
                print(err.message)
                print("#######################################The following file was not indexed: "+filename)
            counter += 1
        # Commit all documents to the index. Optimise and merge best set to True in case of bulk documents.
        writer.commit(optimize=optimise, merge=merge)
        print(str(counter)+" document(s) added")

    def write_single_index(self, file_path, list_of_fields=None):
        """
        Add a single document to the existing index
        :param directory_path:
        :param list_of_fields:
        :return:
        """

        # writer to write index
        if list_of_fields is None:
            list_of_fields = LIST_OF_FIELDS
        writer = self.ix.writer()
        # get data from file
        data = self.index_doc(file_path, list_of_fields)
        # writer.add_document(overview=data['overview'], tagline=data['tagline'], title=data['title'], production_companies=data['production_companies'], \
        #                     genres=data['genres'], runtime=data['runtime'], poster_path=data['poster_path'], imdb_id=data['imdb_id'], popularity=data['popularity'],\
        #                     revenue=data['revenue'], vote_average=data['vote_average'], adult=data['adult'], release_date=data['release_date'])

        # Was used in python 2.7 to support unicode encoding
        writer.add_document(overview=unicode(data['overview']), tagline=unicode(data['tagline']), title=unicode(data['title']), production_companies=unicode(data['production_companies']), \
                            genres=unicode(data['genres']), runtime=unicode(data['runtime']), poster_path=unicode(data['poster_path']), imdb_id=unicode(data['imdb_id']), popularity=unicode(data['popularity']),\
                            revenue=unicode(data['revenue']), vote_average=unicode(data['vote_average']), adult=unicode(data['adult']), release_date=unicode(data['release_date']))
        writer.commit()
        print("Document added")


def start_indexing(index_file, document_path, no_directory, new_index):
    if new_index:
        print("Creating a new index...")
        index_obj = Indexing(index_file, True)
    else:
        print("Opening previous index...")
        index_obj = Indexing(index_file, False)

    if no_directory:
        print("Indexing files from directory...")
        index_obj.write_index(document_path, LIST_OF_FIELDS)
    else:
        print("Writing single file...")
        index_obj.write_single_index(document_path, LIST_OF_FIELDS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create index from a list of documents or add to existing index')
    parser.add_argument('--index_file', default=None, help='The path to index file')
    parser.add_argument('--document_path', default=None, help='Path to directory of documents/document')
    parser.add_argument('--no_directory', action='store_false', default=True, help='Points to a directory of documents')
    parser.add_argument('--new_index', action='store_true', default=False, help='Creating a new index')

    start_indexing(**parser.parse_args().__dict__)


