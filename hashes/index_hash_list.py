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
    for line in f.readlines():
        split = line.split(',')
        ioi_string = split[1].rstrip()
        mapping[split[0]] = ioi_string

    possible_extensions: Dict[str, List[str]] = dict()
    for hash_name in mapping:
        hash = hash_name[:-5]
        if hash not in possible_extensions:
            possible_extensions[hash] = [hash_name[-4:]]
        else:
            possible_extensions[hash].append(hash_name[-4:])

    for k in possible_extensions:
        if len(possible_extensions[k]) > 1:
            print("My assumption that the hashes aren't dependent on the extension is wrong: ", k, possible_extensions[k])

    with open('./mapping.pickle', 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)