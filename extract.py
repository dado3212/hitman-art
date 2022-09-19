from os import listdir
from os.path import isfile, join, getsize
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
 
file_size = getsize(rpkg)

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

patch_offset = f.tell()

if ((version == 1 and file_size <= 0x14) or version == 2 and file_size <= 0x1D):
    exit("Empty RPKG file?")

if (version == 1 and patch_count * 8 + 0x24 >= file_size):
    is_patch_file = False
elif (version == 2 and patch_count * 8 + 0x2D >= file_size):
    is_patch_file = False
else:
    if (version == 1):
        f.seek(patch_count * 8 + 0x1B)
    else:
        f.seek(patch_count * 8 + 0x24)
    test_zero_value = int.from_bytes(f.read(1), 'little')
    test_header_offset = int.from_bytes(f.read(8), 'little')
    print(test_zero_value)
    print(test_header_offset)
    if (
        version == 1 and 
        test_header_offset == (hash_header_table_size + hash_resource_table_size + patch_count * 8 + 0x14)
        and test_zero_value == 0
    ):
        is_patch_file = True
    elif (
        version == 2 and 
        test_header_offset == (hash_header_table_size + hash_resource_table_size + patch_count * 8 + 0x1D)
        and test_zero_value == 0
    ):
        is_patch_file = True
    else:
        # Default value
        is_patch_file = False
    
print(is_patch_file)
print(file_size)
'''

    // Read in the patch list if RPKG is a patch file with a non zero patch list
    if (rpkgs.back().is_patch_file)
    {
        if (rpkgs.back().header.patch_count > 0)
        {
            rpkg_file.SeekTo(patch_offset);
            rpkgs.back().patch_entry_list.resize(rpkgs.back().header.patch_count);
            rpkg_file.Read<uint64_t>(rpkgs.back().patch_entry_list.data(), rpkgs.back().header.patch_count);
        }
    }

    std::string import_text = "Importing RPKG file: " + rpkgs.back().rpkg_file_name;
    LOG_NO_ENDL(import_text);

    // Seek to the hash data table's offset
    size_t hash_data_offset = 0x10;
    if (rpkgs.back().rpkg_file_version == 2)
        hash_data_offset += 9;
    if (rpkgs.back().is_patch_file)
        hash_data_offset += rpkgs.back().header.patch_count * 8 + 4;

    rpkg_file.SeekTo(hash_data_offset);

    // Read both RPKG's hash tables at once into a temporary char buffer
    size_t hash_tables_combined_size = rpkgs.back().header.hash_header_table_size + rpkgs.back().header.hash_resource_table_size;
    std::vector<char> hash_tables(hash_tables_combined_size, 0);
    rpkg_file.Read<char>(hash_tables.data(), hash_tables_combined_size);

    // Load RPKG's hash tables in StreamReader
    StreamReader hash_tables_stream(hash_tables.data(), hash_tables.size());

    // Init timer
    std::chrono::time_point start_time = std::chrono::high_resolution_clock::now();
    int stringstream_length = 80;

    // Read in the hash files/resources data tables
    for (size_t i = 0; i < rpkgs.back().header.hash_count; i++)
    {
        // Emplace back new hash in rpkg
        rpkgs.back().hash.emplace_back();

        hash_tables_stream.Read<hash::HashHeader>(&rpkgs.back().hash.back().data.header);

        rpkgs.back().hash_map[rpkgs.back().hash.back().data.header.hash] = (uint64_t)rpkgs.back().hash_map.size();
    }

    // Emplace back the hash depends map
    hashes_depends_map.emplace_back();

    // Read in the hash files/resources info tables
    for (size_t i = 0; i < rpkgs.back().header.hash_count; i++)
    {
        //HashInfo hash_info;
        hash_tables_stream.Read<hash::HashResource>(&rpkgs.back().hash[i].data.resource);

        // Reverse the hash's resource type string
        char type[4];
        std::memcpy(&type, rpkgs.back().hash[i].data.resource.resource_type, 4);
        rpkgs.back().hash[i].data.resource.resource_type[0] = type[3];
        rpkgs.back().hash[i].data.resource.resource_type[1] = type[2];
        rpkgs.back().hash[i].data.resource.resource_type[2] = type[1];
        rpkgs.back().hash[i].data.resource.resource_type[3] = type[0];

        // Determine hash's size and if it is LZ4ed and/or XORed
        if ((rpkgs.back().hash[i].data.header.data_size & 0x3FFFFFFF) != 0)
        {
            rpkgs.back().hash[i].data.lz4ed = true;
            rpkgs.back().hash[i].data.size = rpkgs.back().hash[i].data.header.data_size;

            if ((rpkgs.back().hash[i].data.header.data_size & 0x80000000) == 0x80000000)
            {
                rpkgs.back().hash[i].data.size &= 0x3FFFFFFF;
                rpkgs.back().hash[i].data.xored = true;
            }
        }
        else
        {
            rpkgs.back().hash[i].data.size = rpkgs.back().hash[i].data.resource.size_final;

            if ((rpkgs.back().hash[i].data.header.data_size & 0x80000000) == 0x80000000)
                rpkgs.back().hash[i].data.xored = true;
        }

        rpkgs.back().hash[i].hash_value = rpkgs.back().hash[i].data.header.hash;
        rpkgs.back().hash[i].hash_resource_type = std::string(rpkgs.back().hash[i].data.resource.resource_type, 4);

        if (rpkgs.back().hash_resource_types.size() > 0)
        {
            bool found = false;

            for (uint32_t j = 0; j < rpkgs.back().hash_resource_types.size(); j++)
            {
                if (rpkgs.back().hash_resource_types.at(j) == rpkgs.back().hash[i].hash_resource_type)
                {
                    found = true;
                    rpkgs.back().hash_resource_types_data_size.at(j) += rpkgs.back().hash[i].data.size;
                    rpkgs.back().hashes_indexes_based_on_resource_types.at(j).push_back(i);
                    rpkgs.back().hashes_based_on_resource_types.at(j).push_back(rpkgs.back().hash[i].data.header.hash);
                }
            }

            if (!found)
            {
                rpkgs.back().hash_resource_types.push_back(rpkgs.back().hash[i].hash_resource_type);
                rpkgs.back().hash_resource_types_data_size.push_back(rpkgs.back().hash[i].data.size);
                std::vector<uint64_t> temp_hashes_indexes_based_on_resource_types;
                temp_hashes_indexes_based_on_resource_types.push_back(i);
                rpkgs.back().hashes_indexes_based_on_resource_types.push_back(temp_hashes_indexes_based_on_resource_types);
                std::vector<uint64_t> temp_hashes_based_on_resource_types;
                temp_hashes_based_on_resource_types.push_back(rpkgs.back().hash[i].data.header.hash);
                rpkgs.back().hashes_based_on_resource_types.push_back(temp_hashes_based_on_resource_types);
            }
        }
        else
        {
            rpkgs.back().hash_resource_types.push_back(rpkgs.back().hash[i].hash_resource_type);
            rpkgs.back().hash_resource_types_data_size.push_back(rpkgs.back().hash[i].data.size);
            std::vector<uint64_t> temp_hashes_indexes_based_on_resource_types;
            temp_hashes_indexes_based_on_resource_types.push_back(i);
            rpkgs.back().hashes_indexes_based_on_resource_types.push_back(temp_hashes_indexes_based_on_resource_types);
            std::vector<uint64_t> temp_hashes_based_on_resource_types;
            temp_hashes_based_on_resource_types.push_back(rpkgs.back().hash[i].data.header.hash);
            rpkgs.back().hashes_based_on_resource_types.push_back(temp_hashes_based_on_resource_types);
        }

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