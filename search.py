from RPKG import RPKG
import pickle, re
from typing import Optional, Pattern

with open('hashes/mapping.pickle', 'rb') as handle:
    mapping = pickle.load(handle)

def search(rpkg: RPKG, search_string: Pattern[str], type: Optional[str] = None):
    for i in rpkg.hashes:
        hash_name = rpkg.hashes[i].getHexName()
        if hash_name not in mapping:
            # TODO: This is super weird, am I not invalidating properly with
            # patches?
            continue
        ioi_string = mapping[hash_name]
        if re.search(search_string, ioi_string):
            if type is None:
                matches_type = True
            else:
                matches_type = (rpkg.hashes[i].hash_resource_type == type)
            if matches_type:
                reference_data = rpkg.hashes[i].hash_reference_data
                if reference_data is not None:
                    for i in range(len(reference_data.hash_reference)):
                        hex = format(reference_data.hash_reference[i], 'x').upper().rjust(16, '0')
                        print(reference_data.hash_reference[i], hex, reference_data.hash_reference_type[i])
                print(ioi_string, i, hash_name)
            
    return None
