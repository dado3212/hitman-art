from RPKG import RPKG
import pickle, re
from typing import Optional, Pattern, Dict, List
from Hash import Hash

with open('rpkg/mapping.pickle', 'rb') as handle:
    mapping: Dict[int, str] = pickle.load(handle)

def guess_name(rpkg: RPKG, hash: int) -> str:
    # First, we'll do it trivially. Check if it's in the mapping
    ioi_string = mapping[hash]
    if len(ioi_string) > 0:
        return ioi_string
    # If it's not, check what files depend on it
    if hash not in rpkg.reverse_dependencies:
        # Usually doesn't have dependencies
        return ''
    for parent in rpkg.reverse_dependencies[hash]:
        possible_ioi_string = mapping[parent]
        return '[?] ' + possible_ioi_string
    return ''

def search(rpkg: RPKG, search_string: Pattern[str], type: Optional[str] = None) -> List[Hash]:
    matches: List[Hash] = []
    for i in rpkg.hashes:
        if rpkg.hashes[i].hash_value not in mapping:
            # TODO: This is super weird, am I not invalidating properly with
            # patches?
            exit("What the hell is " + str(rpkg.hashes[i].hash_value))
        ioi_string = guess_name(rpkg, rpkg.hashes[i].hash_value)
        if re.search(search_string, ioi_string):
            if type is None:
                matches_type = True
            else:
                matches_type = (rpkg.hashes[i].hash_resource_type == type)
            if matches_type:
                if ('[?] ' in ioi_string):
                    print(ioi_string, rpkg.hashes[i].getHexName())
                matches.append(rpkg.hashes[i])
            
    return matches
