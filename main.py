from os import listdir
from os.path import isfile, join
from extract import extract

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]
# TODO: FIX THIS, ONLY FOR TESTING
rpkgs = ['chunk21patch2.rpkg']

rpkg_path = join(directory, rpkgs[0])
rpkg = extract(rpkgs[0], rpkg_path)

for i in rpkg.hashes:
    print(rpkg.hashes[i].getHexName())

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