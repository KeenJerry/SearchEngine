# def calculateQueryTf(query):
#     tfs = {}
#     for query_term in list(set(query)): # assume query is a list of string
#         tfs.update({query_term: query.count(query_term)})
#     return tfs

import math
from MaxHeap import MaxHeap

def fastCosineScore(query, data, docs):
    max_heap = MaxHeap()
    scores = {}
    for doc in docs:
        scores.update({doc.id: 0})
    for query_term in list(set(query)):
        wtq = math.log(data[2][query_term]) # assume data to be [postings, tf_info, idf_info] and idf_info to be N/dfi
        postings_list = data[0][query_term]
        tfs = data[1][query_term]
        for key, value in postings_list:
            scores[key] += tfs[key] * wtq
    for key, value in scores:
        value /= docs.find(key).length
        max_heap.insert({key, value})
    return max_heap.maxK()
