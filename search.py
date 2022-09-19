from RPKG import RPKG
import pickle, re
from typing import Optional, Pattern, Dict

with open('hashes/mapping.pickle', 'rb') as handle:
    mapping: Dict[int, str] = pickle.load(handle)


def guess_name(rpkg: RPKG, hash: int) -> str:
    # First, we'll do it trivially. Check if it's in the mapping
    ioi_string = mapping[hash]
    if len(ioi_string) > 0:
        return ioi_string
    # If it's not, check what files depend on it
    for parent in rpkg.reverse_dependencies[hash]:
        possible_ioi_string = mapping[parent]
        print(possible_ioi_string)
    return ''

def search(rpkg: RPKG, search_string: Pattern[str], type: Optional[str] = None):
    for i in rpkg.hashes:
        if rpkg.hashes[i].hash_value not in mapping:
            # TODO: This is super weird, am I not invalidating properly with
            # patches?
            exit("What the hell is " + str(rpkg.hashes[i].hash_value))
        ioi_string = mapping[rpkg.hashes[i].hash_value]
        if re.search(search_string, ioi_string):
            if type is None:
                matches_type = True
            else:
                matches_type = (rpkg.hashes[i].hash_resource_type == type)
            if matches_type:
                for dependency in rpkg.hashes[i].getDependencies():
                    hex = format(dependency, 'x').upper().rjust(16, '0')
                    print(dependency, hex, guess_name(rpkg, dependency))
                print(ioi_string, i, rpkg.hashes[i].getHexName())
            
    return None
