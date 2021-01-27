import numpy as np
from classification.bert import todo_melanger, getTitleCheck_BERT
from vgg16_p.newvgg import compare_melanger, getTitleCheck_VGG

def todo_all(text, search_type,):
    sim_bert = todo_melanger(text, search_type)
    sim_vgg = compare_melanger()
    title_bert = getTitleCheck_BERT()
    title_vgg = getTitleCheck_VGG()
    recommand = []
    tmp = {}
    for i in title_bert.keys():
        if i in title_vgg.keys():
            res = sim_bert[title_bert[i]] + sim_vgg[title_vgg[i]]
            del title_bert[i]
            del title_vgg[i]
            tmp[i] = res
        else:
            res = sim_bert[title_bert[i]]
            del title_bert[i]
            tmp[i] = res
    for i in title_vgg.keys():
        tmp[i] = sim_vgg[title_vgg[i]]
    a = sorted(tmp.items(), key = lambda kv:(kv[1]), reverse = True)
    for i in range(10):
        recommand.append(a[i][0])
    return recommand

