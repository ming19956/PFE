import numpy as np
from classification.bert import todo_melanger, getTitleCheck_BERT, getMain_info
from vgg16_p.newvgg import compare_melanger, getTitleCheck_VGG
import numpy as np
def todo_all(text, search_type):
    sim_bert = todo_melanger(text)
    main_info_bert = getMain_info()
    print(main_info_bert)
    sim_vgg = compare_melanger()

    title_bert = getTitleCheck_BERT()
    title_vgg = getTitleCheck_VGG()
    recommand = []
    tmp = {}
    flag = 0
    for i in title_bert.values():
        if '0' not in search_type:
            if main_info_bert[flag] == 'title':
                flag += 1
                continue
        elif '1' not in search_type:
            if main_info_bert[flag] == 'content':
                flag += 1
                continue
        i = int(i)
        if i in title_vgg.values():
            vgg_n = list(title_vgg.keys())[list(title_vgg.values()).index(int(i))]
            res = sim_bert[-1, flag] + sim_vgg[-1, vgg_n]
            tmp[i] = res
        else:
            res = sim_bert[-1, flag]
            tmp[i] = res
        flag += 1

    a = sorted(tmp.items(), key = lambda kv:(kv[1]), reverse = True)
    print(np.shape(a))
    for i in range(10):
        recommand.append(a[i][0])
    return recommand

