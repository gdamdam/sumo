from __future__ import division
from tools import connector

import math

MIN_LENG = 2            # minumum number of shared elements
CLUSTER_ELEMENTS = 10   # number of documents part of a cluste




def get_cluster(doc_url_name):
    """ Function create the cluster of the N document using the euclidean distance

    Args:
        doc_url_name

    Returns:
        the dictionary with the cluster of the N documents
    """
    cluster = {}
    euc_distance = {}

    data1 = connector.mongo_find(doc_url_name)
    vect1 = data1['most_freq_stem_words_wn']
    documents = connector.mongo_all(1000)
    for i in documents:
        if documents[i] != doc_url_name:
            data2 = connector.mongo_find(documents[i])
            vect2 = data2['most_freq_stem_words_wn']
            if vect2 !='':
                dist = _euc(vect1,vect2)
                if dist['score'] != 'NULL':
                    euc_distance[documents[i]] = dist

    cluster = sorted(euc_distance.items(),key=lambda x: x[1]['score'])[:CLUSTER_ELEMENTS]

    return dict(cluster)




def _euc(diz1,diz2):
    """ Function returns the euclidean distance between two dictionries

    Args:
        diz1 and diz2

    Resturs:
        a score based on the euclidean distance 
    """
    euc_dist = {}
    keys1 = diz1.keys()
    keys2 = diz2.keys()
    k_inter = (set(keys1) & set(keys2))
    if len(k_inter) >= MIN_LENG:
        dist = math.sqrt(sum((diz1[k] - diz2[k])**2 for k in k_inter))
        score = dist/(len(keys1)+len(keys2))
    else:
        score = 'NULL'

    euc_dist['intersection'] = list(k_inter)
    euc_dist['score'] = score

    return euc_dist

