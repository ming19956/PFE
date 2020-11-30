# coding=utf-8
import ast
import json
# a = ast.literal_eval('{"genres":[{"id":35,"name":"Comedy"},{"id":18,"name":"Drama"}]}')
# print (a['genres'])

def unicode_convert(input):
    if isinstance(input, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


with open("/Users/yma/Documents/python/machinelearning/info-retrival-search-engine/trial/movie_99.json") as f:
    a = json.load(f)
    sep = json.dumps(a, ensure_ascii=False)
    #c = unicode_convert(json.loads(sep))
    c = json.loads(sep)
    prod = []
    print(c['genres'][0]['name'])
    print(type(c['genres'][0]))
    for x in c["production_companies"]:
        prod.append(x['name'])
    print(prod)

