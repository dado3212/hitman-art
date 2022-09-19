from os import listdir
from os.path import isfile, join
from extract import extract
from search import search
import re
from utils import hash_to_hex

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs_names = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]
# TODO: Just for testing
# rpkgs_names = ['chunk21patch2.rpkg']
rpkgs_names = ['chunk24.rpkg', 'chunk3.rpkg']

download_code = ''
for rpkg_name in rpkgs_names:
    rpkg_path = join(directory, rpkg_name)
    rpkg = extract(rpkg_name, rpkg_path)

    pattern = re.compile("hotel_room_thai_a_decal")
    hashes = search(rpkg, pattern, "TEXT")
    for hash in hashes:
        download_code += './rpkg-cli.exe -filter ' + hash_to_hex(hash.hash_value) + ' -extract_from_rpkg "' + directory + '\\' + rpkg_name + '"\n'

print(download_code)