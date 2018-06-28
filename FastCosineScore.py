# def calculateQueryTf(query):
#     tfs = {}
#     for query_term in list(set(query)): # assume query is a list of string
#         tfs.update({query_term: query.count(query_term)})
#     return tfs

# task to do
# 1. generateChampionList
# 2. remove docs in fastCosineScore parameters DONE
# 3. the high and the low champion list

import math
from MaxHeap import MaxHeap

index_elimination_threshold = 0.5 # ???
r = 10 # ???

# def generateChampionList(data):
#     new_tf_info = {}
#     for term, tfs in data[1].iterms():
#         new_tfs_info = {tp[0]:tp[1]} for tp in sorted(tfs.items(), key=lambda x:x[1], reverse=True)[:(r + 1)]}
#         new_tf_info.update({term: new_tfs_info})
#     return [data[0], new_tf_info, data[2]]

def fastCosineScore(query, data, docs, index_elimination=False):
    scores = {}
    max_heap = MaxHeap()
    for query_term in list(set(query)):
        if index_elimination:
            if math.log(data[2][query_term]) < index_elimination_threshold:
                continue
        wtq = math.log(data[2][query_term]) # assume data to be [postings, tf_info, idf_info] and idf_info to be N/dfi
        # postings_list = data[0][query_term]
        tfs = data[1][query_term]
        for id, tf in tfs.items():
            if id == -1:
                continue
            if scores.has_key(id):
                scores[id] += tf * wtq
            else:
                scores.update({id: tf * wtq})
    for id, score in scores.items():
        score /= docs.find(id).length # definition of docs UNKNOWN
        max_heap.insert({id, score})
    return max_heap.maxK()

def fastCosineScoreWithChampionList(query, data, docs, index_elimination=False):
    return fastCosineScore(query, generateChampionList(data), docs, index_elimination=index_elimination)
