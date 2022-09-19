import unittest
from utils import hex_to_hash, hash_to_hex

class UtilsTest(unittest.TestCase):

    def test_hex_to_hash(self):
        self.assertEqual(hex_to_hash('0023432D2C4E9603'), 9925485480809987)
        self.assertEqual(hex_to_hash('0015166FD329DF6C'), 5935644050841452)

    def test_hash_to_hex(self):
        self.assertEqual(hash_to_hex(9925485480809987), '0023432D2C4E9603')
        self.assertEqual(hash_to_hex(5935644050841452), '0015166FD329DF6C')

if __name__ == '__main__':
    unittest.main()