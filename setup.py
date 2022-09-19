import pickle, os, requests, json, zipfile
from typing import Dict
from utils import hex_to_hash

if os.path.exists('./rpkg'):
    print("rpkg folder already exists. If you want to update, just delete it.")
    exit()

# Download rpkg
rpkg_tool_info = json.loads(requests.get('https://api.github.com/repos/glacier-modding/RPKG-Tool/releases/latest').text)
download_links = [x['browser_download_url'] for x in rpkg_tool_info['assets'] if 'src' not in x['name']]
if (len(download_links) != 1):
    print("Something went wrong with downloading rpkg.")
    exit()

r = requests.get(download_links[0], stream=True)
with open('rpkg.zip', 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

with zipfile.ZipFile('rpkg.zip') as zf:
    zf.extractall('rpkg')

os.remove('rpkg.zip')

# This is intended to be run just once whenever hash_list.txt is updated.
with open('./rpkg/hash_list.txt', 'r') as f:
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

    with open('./rpkg/mapping.pickle', 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)