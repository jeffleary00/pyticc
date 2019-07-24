#!/usr/bin/env python3

import unittest
from pyticc.utils import byte_bit_value, bit_into_byte

class TestUtil(unittest.TestCase):
# ###############################################

    def test_byte_bit_01(self):
        """Test proper extraction of bit values from byte"""

        assert byte_bit_value(0x05, (7,1)) == 1

    def test_byte_bit_02(self):
        """Test more proper extraction of bit values from byte"""
        assert byte_bit_value(0xFF, (0,8)) == 0xFF

    def test_bit_into_byte(self):
        """Test proper insertion of bit values into a byte"""
        assert bit_into_byte(0x09, (5,2), "11") == 0x0F

if __name__ == '__main__':
    unittest.main()
