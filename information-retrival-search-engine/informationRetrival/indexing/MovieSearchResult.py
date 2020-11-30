

class SearchResult:

    def __init__(self, original_query=""):
        self.original_query = original_query
        self.corrected_query = ''
        self.title_result = []
        self.overview_result = []
        self.tagline_result = []
        self.genre_result = []
        self.review_result = []
        self.suggested_spelling=dict()

    def set_item(self, key, value):
        if key == "title":
            self.title_result = value
        elif key == "overview":
            self.overview_result = value
        elif key == "tagline":
            self.tagline_result = value
        elif key == "genres":
            self.genre_result = value
        elif key == "review":
            self.review_result = value
        elif key == "suggested_spelling":
            self.suggested_spelling = value
        else:
            return False
        return True
