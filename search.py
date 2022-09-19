from RPKG import RPKG
import pickle

with open('hashes/mapping.pickle', 'rb') as handle:
    mapping = pickle.load(handle)
with open('hashes/no_name.pickle', 'rb') as handle:
    no_name = pickle.load(handle)

def search(rpkg: RPKG, search_string: str):
    for k in mapping:
        if search_string in k:
            hex_file_path = mapping[k]
            for i in rpkg.hashes:
                if rpkg.hashes[i].getHexName() == hex_file_path:
                    print(rpkg.hashes[i], i, hex_file_path)
    return None
