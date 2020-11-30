import ast
import json

class MovieData:

    def __init__(self, source):
        """
        :param source: The path of the data file
        """
        self.source=source
        self.data_ast=self.__parseFile__(source)

    def __parseFile__(self, source):
        """
        Parses the given data file and stores the ast
        :param source: The path of the data file
        :return:
        """
        try:
            for i in open(source, mode='r').read():
                print(i)
            #print(ast.literal_eval(open(source, mode='r').read()))
            #return ast.literal_eval(open(source, mode='r').read())
        except Exception as err:
            print ("Improper file syntax: "+source)
            return None

    def get(self, name_of_field):
        """
        Retrievs the value corresponding to the given field name
        :param name_of_field:
        :return:
        value of the api field required if it exists, None otherwise
        """
        return self.data_ast.get(name_of_field)