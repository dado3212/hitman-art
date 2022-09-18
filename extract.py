from os import listdir
from os.path import isfile, join
import subprocess

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]
# TODO: FIX THIS, ONLY FOR TESTING
rpkgs = ['chunk21patch2.rpkg']

rpkg = join(directory, rpkgs[0])
print(rpkg)

# Load up the RPKG
# Adapted from import_rpkg in RPKG-Tool
f = open(rpkg, 'rb')

# Read the version
raw_version = f.read(4)
version = -1
if (raw_version.decode("utf-8")  == 'GKPR'):
    version = 1
elif (raw_version.decode("utf-8")  == '2KPR'):
    version = 2
    header = f.read(9)
else:
    exit("Not sure how to read this")

# From rpkg_src/rpkg.h, Header is composed of 4 uint32_t's, representing 
# hash count, hash_header_table_size, hash_resource_table_size, patch count
hash_count = int.from_bytes(f.read(4), 'little')
hash_header_table_size = int.from_bytes(f.read(4), 'little')
hash_resource_table_size = int.from_bytes(f.read(4), 'little')
patch_count = int.from_bytes(f.read(4), 'little')
print(hash_count)
print(hash_header_table_size)
print(hash_resource_table_size)
print(patch_count)

f.close()
exit()

# For each rpkg search specifically for TEXT that matches
list_files = subprocess.run(
    [
        "../rpkg_v2.24.0/rpkg-cli.exe",
        # "-filter", "TEXT",
        "-regex_search", "\"assembly:.*paintings.*diffuse_.*\"",
        "-search_rpkg", join(directory, rpkgs[0])
    ])
    #, stdout=subprocess.DEVNULL)

print(list_files)
# rpkg-cli.exe -filter TEXT -regex_search "assembly:.*paintings.*diffuse_.*" -search_rpkg 