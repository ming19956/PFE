from datetime import  datetime
from whoosh.qparser import QueryParser
from whoosh import index
from whoosh import scoring

from whoosh.qparser.dateparse import DateParserPlugin
import whoosh.query as query
from MovieSearchResult import SearchResult


class Search:

    def __init__(self, index_file):
        try:
            self.ix = index.open_dir(index_file)
            self.search_result = SearchResult()
        except OSError as err:
            print (err.message)

    def search_doc(self, field_key, query_string, number_of_results=100, get_more_suggestions=False):
        """
        Function to search a document
        :param field_key: key to search
        :param query_string: the user provided  query
        :param number_of_results: Default upto 100 results, can be modified
        :param get_more_suggestions: Set True in order to get more than one suggestion for did you mean for interactive user search
        """
        # Stores original query
        self.search_result.original_query = query_string
        # Query initialization
        qp = QueryParser(field_key, schema=self.ix.schema)
        qp.add_plugin(DateParserPlugin())
        q = qp.parse(query_string)
        # old_query = query.DateRange("release_date",datetime.strptime("1995","%Y"),datetime.strptime("2000","%Y"))
        # allow_query = query.NumericRange("vote_average",5, 10)
        # allow_query = query.Require(old_query,allow_query)
        # Only as long as 's' is open we can access results (iterator is returned)
        with self.ix.searcher(weighting=scoring.TF_IDF()) as s:
                # checks query for spelling errors
                corrected = s.correct_query(q, query_string)
                if corrected.query != q:
                    self.search_result.corrected_query = "Did you mean:" + corrected.string
                    # Updates query with closest corrected version
                    q = qp.parse(corrected.string)
                    # If more than one suggestion is required for spelling check
                    if get_more_suggestions:
                        suggestions = self.get_more_suggestions(query_string, field_key, corrected.string, s)
                        self.search_result.set_item("suggested_spelling", suggestions)
                # gets final search result from index
                results = s.search(q) #, filter = allow_query,limit=number_of_results)

                # Makeshift function for now, in order to store iterator in the search_result
                print (results[:5])
                print (len(results))
                # Stores result as a list
                self.search_result.set_item(field_key, list(results))


    @staticmethod
    def get_more_suggestions(query_string, field_key, corrected_string, s):
        # Stores list of words with spelling error detected
        mistyped_words = []
        # for each word from original query
        for word in query_string.split(" "):
            # if the word id mis-spelt, store it
            if word not in corrected_string:
                mistyped_words.append(word)
        # initialize the corrector
        corrector = s.corrector(field_key)
        # stores mapping of incorrect->list of correct words
        list_of_corrections = dict()
        # Retrieves top 3 closest word based on existing index
        for mistyped_word in mistyped_words:
            list_of_corrections[mistyped_word] = corrector.suggest(mistyped_word, limit=5)
        return list_of_corrections

FILEPATH="/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/Index_tmp"
so=Search(FILEPATH)
res = so.search_doc("title","All about my monther",get_more_suggestions=False)
print (so.search_result.corrected_query)
print (so.search_result.suggested_spelling)
print (len(so.search_result.overview_result))

