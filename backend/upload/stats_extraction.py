from collections import defaultdict  # available in Python 2.5 and newer
from .DB_operations import extract_coll_stats, extract_coll_quantity

def extract_for_stats(db):
    fname_list, art_list = extract_coll_stats(db)
    coll_d = extract_coll_quantity(db)
    fname_d = fname_extraction(fname_list)
    art_d = art_extraction(art_list)
    #print(f'coll_d : {coll_d}')
    #print(f'fname_d : {fname_d}')
    #print(f'art_d : {art_d}')
    tot_d = dict()
    tot_d['coll_d'] = coll_d
    tot_d['fname_d'] = fname_d
    tot_d['art_d'] = art_d
    return tot_d



def fname_extraction(fname_list):
    fname_d = defaultdict(int)
    for elem in fname_list:
        fname_d[elem] += 1
    return dict(fname_d)


def art_extraction(art_list):
    art_d = defaultdict(int)
    for elem in art_list:
        art_d[elem] += 1
    return dict(art_d)

