import os
from MovieData import MovieData


class ParseData:

    def __init__(self, directory):
        self.directory = directory

    def parse_directory(self):
        """
        Parses every file in the given directory
        :return:
        """
        for filename in os.listdir(self.directory):
            # combining the path names
            file_path = os.path.join(self.directory, filename)
            self.parse_file(file_path)

    def parse_file(self, filename, current_directory=True):
        """
        Parses a single file

        :param filename: name of the file in the initialized directory or full path of the fil
        :param current_directory: Default True, set false if full path of file specified under filename
        :return:
        """
        if current_directory:
            file_path = os.path.join(self.directory, filename)
        current_item = MovieData(file_path)
        if current_item is not None:
            pass
            # TODO 1: Replace pass and implement function to read into index


