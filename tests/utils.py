#!/usr/bin/env python3

import unittest
from pyticc.utils import byte_bit_value, bit_into_byte

class TestUtil(unittest.TestCase):
# ###############################################

    def test_byte_bit_01(self):
        assert byte_bit_value(0x05, (7,1)) == 1

    def test_byte_bit_02(self):
        assert byte_bit_value(0xFF, (0,8)) == 0xFF

    def test_bit_into_byte(self):
        assert bit_into_byte(0x09, (5,2), "11") == 0x0F

if __name__ == '__main__':
    unittest.main()
