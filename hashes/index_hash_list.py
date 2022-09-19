import pickle
from typing import Dict, List

# This is intended to be run just once whenever hash_list.txt is updated.
with open('hash_list.txt', 'r') as f:
    # completion
    f.readline()
    # hashes count
    f.readline()
    # version number
    f.readline()
    # actual lines
    mapping: Dict[str, str] = dict()
    no_name: List[str] = []
    for line in f.readlines():
        split = line.split(',')
        ioi_string = split[1].rstrip()
        mapping[split[0]] = ioi_string

    with open('./mapping.pickle', 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)