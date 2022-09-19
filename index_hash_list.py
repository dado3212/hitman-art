import pickle
from typing import Dict
from utils import hex_to_hash

# This is intended to be run just once whenever hash_list.txt is updated.
with open('./hashes/hash_list.txt', 'r') as f:
    # completion
    f.readline()
    # hashes count
    f.readline()
    # version number
    f.readline()
    # actual lines
    mapping: Dict[int, str] = dict()
    possible_extensions: Dict[str, str] = dict()
    for line in f.readlines():
        split = line.split(',')
        ioi_string = split[1].rstrip()
        hex = split[0][:-5]
        extension = split[0][:-4]

        if hex not in possible_extensions:
            possible_extensions[hex] = extension
        else:
            exit("My assumption that the hashes aren't dependent on the extension is wrong: " + hex + ' can have two extensions, ' + possible_extensions[hex] + ' and ' + extension)

        mapping[hex_to_hash(hex)] = ioi_string

    with open('./hashes/mapping.pickle', 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)