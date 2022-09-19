from os import listdir, walk, mkdir
from os.path import isfile, join, expanduser
from extract import extract
from search import search
import re, subprocess, shutil
from utils import hash_to_hex
from PIL import Image

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs_names = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]

# Clear the output folder
shutil.rmtree('./output', ignore_errors=True)
shutil.rmtree('./tmp', ignore_errors=True)
mkdir('./output')

# Download the raw TGA texture files
for rpkg_name in rpkgs_names:
    print("Looking at ", rpkg_name)
    rpkg_path = join(directory, rpkg_name)
    rpkg = extract(rpkg_name, rpkg_path)

    pattern = re.compile("(paintings|wallart|graffiti|street_art|mural|drawings).*diffuse")
    hashes = search(rpkg, pattern, "TEXT")
    if len(hashes) > 0:
        print("Found " + str(len(hashes)) + " images to download.")
    for hash in hashes:
        # For each rpkg search specifically for TEXT that matches
        download = subprocess.run(
            [
                "./rpkg/rpkg-cli.exe",
                "-filter", hash_to_hex(hash.hash_value),
                "-output_path", './tmp',
                "-extract_text_from", join(directory, rpkg_name)
            ], stdout=subprocess.DEVNULL)

print("Converting images...")
# Convert them into PNG
all_output_files = [join(dp, f) for dp, _, fn in walk(expanduser('./tmp')) for f in fn]
tga_files = [f for f in all_output_files if f.endswith('.tga')]
i = 0
for tga in tga_files:
    im = Image.open(tga)
    im.save('./output/' + str(i) + '.png')
    i += 1

shutil.rmtree('./tmp')
print("Done! Check the 'output' folder.")