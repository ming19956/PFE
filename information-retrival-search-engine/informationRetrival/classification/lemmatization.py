# coding=utf-8
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class lemmatization(object):
    def __init__(self):

        self.lmtzr = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def removeStopWords(self, words):
        """ Removes the stopwords from the given list of words.
        :param words: List of all the words
        :return: the unique words in a list of words after removing stop words
        """
        line = []
        for w in words:
            if w not in self.stop_words:
                line.append(w)
        return line

    def getBiwords(self, words):
        """ Removes all the biwords from the given sentence.
        :param words: List of all the words
        :return: the bigrams from the sentence provided
        """
        bigrams_val = nltk.bigrams(words)
        biwords = []
        for word in bigrams_val:
            biwords.append(word)
        return biwords

    def lemmatizeWord(self, lst):
        """ Lemmatize the list of words.
        :param words: List of all the words
        :return: the lemmatized version of the words
        """
        lemmatized_list = []
        for item in lst:
            lemmatized_list.append(self.lmtzr.lemmatize(item))
        return lemmatized_list