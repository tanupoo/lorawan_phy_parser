#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from LoRaMacPayloadEncrypt import LoRaMacPayloadEncrypt
import binascii

####

class test_LoRaMacPayloadEncrypt(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        buf_hex="CCBFE651AE1E2342466C6D63FC55951C1A392AA413D4C82B5AEA"
        res_hex="00000a0800000000000000000000000000000000000000000000"
        key_hex = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABB"
        fcnt_hex = "0000000d"
        addr_hex = "BEEF00B1"
        r1 = LoRaMacPayloadEncrypt(buf_hex, key_hex, addr_hex, 0, fcnt_hex)
        r2 = binascii.b2a_hex(r1).upper()
        self.assertEqual(r2, res_hex.upper())

    def test_2(self):
        buf_hex="7986"
        res_hex="0002"
        key_hex = "2b7e151628aed2a6abf7158809cf4f3c"
        fcnt_hex = "00000003"
        addr_hex = "0000baad"
        r1 = LoRaMacPayloadEncrypt(buf_hex, key_hex, addr_hex, 1, fcnt_hex)
        r2 = binascii.b2a_hex(r1).upper()
        self.assertEqual(r2, res_hex.upper())

    def test_3(self):
        buf_hex="6e"
        res_hex="00"
        key_hex = "2B7E151628AED2A6ABF7158809CF0811"
        fcnt_hex = "00000008"
        addr_hex = "01460c75"
        r1 = LoRaMacPayloadEncrypt(buf_hex, key_hex, addr_hex, 0, fcnt_hex)
        r2 = binascii.b2a_hex(r1).upper()
        self.assertEqual(r2, res_hex.upper())

if __name__ == '__main__':
    unittest.main()
