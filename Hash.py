from typing import BinaryIO, List

class HashHeader:
    def __init__(self, f: BinaryIO):
        self.hash = int.from_bytes(f.read(8), 'little')
        self.data_offset = int.from_bytes(f.read(8), 'little')
        self.data_size = int.from_bytes(f.read(4), 'little')

class HashResource:
    def __init__(self, f: BinaryIO):
        resource_type_bytes: List[bytes] = []
        for _ in range(4):
            resource_type_bytes.append(f.read(1))
        self.resource_type = "".join([x.decode("utf-8") for x in resource_type_bytes[::-1]])
        self.reference_table_size = int.from_bytes(f.read(4), 'little')
        self.reference_table_dummy = int.from_bytes(f.read(4), 'little')
        self.size_final = int.from_bytes(f.read(4), 'little')
        self.size_in_memory = int.from_bytes(f.read(4), 'little')
        self.size_in_video_memory = int.from_bytes(f.read(4), 'little')

class Hash:
    header: HashHeader
    resource: HashResource
    lz4ed: bool = False
    xored: bool = False
    size: int = 0

    def __init__(self, header: HashHeader):
        self.header = header