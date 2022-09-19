from os import listdir
from os.path import isfile, join
from extract import extract
from search import search
import re

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs_names = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]
# TODO: Just for testing
# rpkgs_names = ['chunk21patch2.rpkg']
rpkgs_names = ['chunk24.rpkg', 'chunk3.rpkg']

for rpkg_name in rpkgs_names:
    rpkg_path = join(directory, rpkg_name)
    rpkg = extract(rpkg_name, rpkg_path)

    # for i in rpkg.hashes:
    #     print(rpkg.hashes[i].getHexName())
    pattern = re.compile("assembly:.*paintings.*diffuse_.*")
    search(rpkg, pattern, 'TEXT')

# # For each rpkg search specifically for TEXT that matches
# list_files = subprocess.run(
#     [
#         "../rpkg_v2.24.0/rpkg-cli.exe",
#         # "-filter", "TEXT",
#         "-regex_search", "\"assembly:.*paintings.*diffuse_.*\"",
#         "-search_rpkg", join(directory, rpkgs[0])
#     ])
#     #, stdout=subprocess.DEVNULL)

# print(list_files)
# # rpkg-cli.exe -filter TEXT -regex_search "assembly:.*paintings.*diffuse_.*" -search_rpkg 