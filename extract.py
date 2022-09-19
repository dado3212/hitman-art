from os import listdir
from os.path import isfile, join, getsize
from typing import List
import subprocess
from Hash import Hash, HashHeader, HashResource, HashReferenceData
from RPKG import RPKG, Header

# File Directory
directory = "D:\\Program Files (x86)\\Epic Games\\HITMAN3\\Runtime"

# Open the directory and determine all of the possible rkpg files
rpkgs = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.rpkg')]
# TODO: FIX THIS, ONLY FOR TESTING
rpkgs = ['chunk21patch2.rpkg']


rpkg_path = join(directory, rpkgs[0])
rpkg = RPKG(rpkgs[0], rpkg_path)

# Load up the RPKG
# Adapted from import_rpkg in RPKG-Tool
f = open(rpkg_path, 'rb')
 
file_size = getsize(rpkg_path)

# Read the version
raw_version = f.read(4)
if (raw_version.decode("utf-8")  == 'GKPR'):
    rpkg.version = 1
elif (raw_version.decode("utf-8")  == '2KPR'):
    rpkg.version = 2
    rpkg.v2_header = f.read(9)
else:
    exit("Not sure how to read this")

rpkg.header = Header(f)
patch_offset = f.tell()

if ((rpkg.version == 1 and file_size <= 0x14) or rpkg.version == 2 and file_size <= 0x1D):
    exit("Empty RPKG file?")

# Determine if it's a patch file
if (rpkg.version == 1 and rpkg.header.patch_count * 8 + 0x24 >= file_size):
    rpkg.is_patch_file = False
elif (rpkg.version == 2 and rpkg.header.patch_count * 8 + 0x2D >= file_size):
    rpkg.is_patch_file = False
else:
    if (rpkg.version == 1):
        f.seek(rpkg.header.patch_count * 8 + 0x1B)
    else:
        f.seek(rpkg.header.patch_count * 8 + 0x24)
    test_zero_value = int.from_bytes(f.read(1), 'little')
    test_header_offset = int.from_bytes(f.read(8), 'little')
    if (
        rpkg.version == 1 and 
        test_header_offset == (rpkg.header.hash_header_table_size + rpkg.header.hash_resource_table_size + rpkg.header.patch_count * 8 + 0x14)
        and test_zero_value == 0
    ):
        rpkg.is_patch_file = True
    elif (
        rpkg.version == 2 and 
        test_header_offset == (rpkg.header.hash_header_table_size + rpkg.header.hash_resource_table_size + rpkg.header.patch_count * 8 + 0x1D)
        and test_zero_value == 0
    ):
        rpkg.is_patch_file = True
    
if (rpkg.is_patch_file):
    if (rpkg.header.patch_count > 0):
        f.seek(patch_offset)
        patch_entry_list: List[int] = []
        for _ in range(0, rpkg.header.patch_count):
            patch_entry_list.append(int.from_bytes(f.read(8), 'little'))
        print(patch_entry_list)

# Seek to the hash data table's offset
hash_data_offset = 0x10
if (rpkg.version == 2):
    hash_data_offset += 9
if (rpkg.is_patch_file):
    hash_data_offset += rpkg.header.patch_count * 8 + 4

f.seek(hash_data_offset)

for i in range(0, rpkg.header.hash_count):
    # Create a new hash
    hash = Hash(HashHeader(f))
    rpkg.hashes[i] = hash

for i in range(rpkg.header.hash_count):
    rpkg.hashes[i].resource = HashResource(f)
    
    # Determine hash's size and if it is LZ4ed and/or XORed
    if (rpkg.hashes[i].header.data_size & 0x3FFFFFFF) != 0:
        rpkg.hashes[i].lz4ed = True
        rpkg.hashes[i].size = rpkg.hashes[i].header.data_size

        if (rpkg.hashes[i].header.data_size & 0x80000000) == 0x80000000:
            rpkg.hashes[i].size &= 0x3FFFFFFF
            rpkg.hashes[i].xored = True
    else:
        rpkg.hashes[i].size = rpkg.hashes[i].resource.size_final
        if (rpkg.hashes[i].header.data_size & 0x80000000) == 0x80000000:
            rpkg.hashes[i].xored = True
    
    rpkg.hashes[i].hash_value = rpkg.hashes[i].header.hash
    rpkg.hashes[i].hash_resource_type = rpkg.hashes[i].resource.resource_type

    found = False
    if len(rpkg.hash_resource_types) > 0:
        # This never happens as of right now
        for j in range(0, len(rpkg.hash_resource_types)):
            if rpkg.hash_resource_types[j] == rpkg.hashes[i].hash_resource_type:
                found = True
                rpkg.hash_resource_types_data_size[j] += rpkg.hashes[i].size
                rpkg.hashes_indexes_based_on_resource_types[j].append(i)
                rpkg.hashes_based_on_resource_types[j].append(rpkg.hashes[i].header.hash)
    if not found:
        rpkg.hash_resource_types.append(rpkg.hashes[i].hash_resource_type)
        rpkg.hash_resource_types_data_size.append(rpkg.hashes[i].size)
        rpkg.hashes_indexes_based_on_resource_types.append([i])
        rpkg.hashes_based_on_resource_types.append([rpkg.hashes[i].header.hash])

    if rpkg.hashes[i].resource.reference_table_size > 0:
        depends_count = int.from_bytes(f.read(4), 'little')
        rpkg.hashes[i].hash_reference_data = HashReferenceData(f)
'''

        if (rpkgs.back().hash[i].data.resource.reference_table_size > 0)
        {
            uint32_t depends_count;
            hash_tables_stream.Read<uint32_t>(&depends_count);
            rpkgs.back().hash[i].hash_reference_data.hash_reference_count = depends_count;
            depends_count &= 0x3FFFFFFF;

            rpkgs.back().hash[i].hash_reference_data.hash_reference_type.resize(depends_count);
            hash_tables_stream.Read<uint8_t>(rpkgs.back().hash[i].hash_reference_data.hash_reference_type.data(), depends_count);

            rpkgs.back().hash[i].hash_reference_data.hash_reference.resize(depends_count);
            hash_tables_stream.Read<uint64_t>(rpkgs.back().hash[i].hash_reference_data.hash_reference.data(), depends_count);

            rpkgs.back().hash[i].hash_reference_data.hash_value = rpkgs.back().hash[i].data.header.hash;

            for (uint64_t j = 0; j < depends_count; j++)
            {
                std::unordered_map<uint64_t, uint64_t>::iterator it = hashes_depends_map.back().find(rpkgs.back().hash[i].hash_reference_data.hash_reference.back());

                if (it == hashes_depends_map.back().end())
                {
                    hashes_depends_map.back()[rpkgs.back().hash[i].hash_reference_data.hash_reference.back()] = hashes_depends_map.back().size();
                }
            }
        }
        else
        {
            rpkgs.back().hash[i].hash_reference_data.hash_reference_count = 0x0;
        }
    }

    hashes_depends_map_rpkg_file_paths.push_back(rpkgs.back().rpkg_file_path);

    if (with_timing)
    {
        std::chrono::time_point end_time = std::chrono::high_resolution_clock::now();

        std::stringstream ss;

        ss << "completed in " << std::fixed << std::setprecision(6) << (0.000000001 * std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count()) << "s";

        LOG(std::string((72 - import_text.length() - ss.str().length()), '.') + ss.str());

        percent_progress = (uint32_t)100;
    }

    task_single_status = TASK_SUCCESSFUL;
'''

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