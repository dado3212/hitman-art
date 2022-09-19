from RPKG import RPKG
import pickle, re
from typing import Optional, Pattern

with open('hashes/mapping.pickle', 'rb') as handle:
    mapping = pickle.load(handle)
with open('hashes/no_name.pickle', 'rb') as handle:
    no_name = pickle.load(handle)

def search(rpkg: RPKG, search_string: Pattern[str], type: Optional[str] = None):
    for ioi_string in mapping:
        if re.search(search_string, ioi_string):
            hex_file_path = mapping[ioi_string]
            for i in rpkg.hashes:
                if rpkg.hashes[i].getHexName() == hex_file_path:
                    if type is None:
                        matches_type = True
                    else:
                        matches_type = (rpkg.hashes[i].hash_resource_type == type)
                    if matches_type:
                        print(ioi_string, i, hex_file_path)
    return None
