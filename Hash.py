class Hash:
    def __init__(self, hash: int, data_offset: int, data_size: int):
        self.hash = hash
        self.data_offset = data_offset
        self.data_size = data_size