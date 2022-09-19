from RPKG import RPKG
import pickle, re
from typing import Optional, Pattern, Dict

with open('hashes/mapping.pickle', 'rb') as handle:
    mapping: Dict[int, str] = pickle.load(handle)


def guess_name(rpkg: RPKG, hash: int) -> str:
    # First, we'll do it trivially. Check if 
    ioi_string = mapping[hash]
    if len(ioi_string) > 0:
        return ioi_string
    print(hash)
    return ''

def search(rpkg: RPKG, search_string: Pattern[str], type: Optional[str] = None):
    for i in rpkg.hashes:
        if rpkg.hashes[i].hash_value not in mapping:
            # TODO: This is super weird, am I not invalidating properly with
            # patches?
            print("What the hell")
            continue
        ioi_string = mapping[rpkg.hashes[i].hash_value]
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
                        print(reference_data.hash_reference[i], hex, reference_data.hash_reference_type[i], guess_name(rpkg, reference_data.hash_reference[i]))
                print(ioi_string, i, rpkg.hashes[i].getHexName())
            
    return None
