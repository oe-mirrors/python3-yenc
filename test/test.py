#!/usr/bin/env python
# -*- coding: utf-8 -*-
##=============================================================================
 #
 # Copyright (C) 2003, 2011 Alessandro Duca <alessandro.duca@gmail.com>
 #
 # This library is free software; you can redistribute it and/or
 #modify it under the terms of the GNU Lesser General Public
 # License as published by the Free Software Foundation; either
 # version 2.1 of the License, or (at your option) any later version.
 #
 # This library is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this library; if not, write to the Free Software
 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 #=============================================================================
 # 
##=============================================================================

import os
import sys
import time
import unittest
from binascii import crc32
from stat import *

import yenc
import _yenc


class BaseTest(object):
    CMD_DATA = "dd if=/dev/urandom of=%s bs=1b count=%d" 
    FILE_E = 'sampledata_e'
    FILE_O = 'sampledata_o'

    def setUp(self):
        os.system(BaseTest.CMD_DATA % (BaseTest.FILE_E, 128))
        os.system(BaseTest.CMD_DATA % (BaseTest.FILE_O, 129))

    def tearDown(self):
        os.unlink(BaseTest.FILE_E)
        os.unlink(BaseTest.FILE_O)
        for x in os.listdir('.'):
            if x.endswith('.out') or x.endswith('.dec'):
                os.unlink(x)


class TestLowLevel(unittest.TestCase):

    def testEncode(self):
        e, c, z = _yenc.encode_string('Hello world!')
        self.assertEquals(e, 'r\x8f\x96\x96\x99J\xa1\x99\x9c\x96\x8eK')
        self.assertEquals(c, 3833259626L)

    def testDecode(self):
        d, c, x = _yenc.decode_string('r\x8f\x96\x96\x99J\xa1\x99\x9c\x96\x8eK')
        self.assertEquals(d, 'Hello world!')
        self.assertEquals(c, 3833259626L)


class TestEncoder(BaseTest, unittest.TestCase):
    pass


class TestDecoder(BaseTest, unittest.TestCase):
    pass


class TestFileFunctions(BaseTest, unittest.TestCase):

    def _readFile(self, filename):
        file_in = open(filename, 'rb')

        data = file_in.read()
        crc_orig = "%08x" % ((crc32(data) ^ 0xFFFFFFFFL) & 0xFFFFFFFFL)
        file_in.close()

        return data, crc_orig


    def _testEncodeFile(self, filename):
        data, crc =  self._readFile(filename)
        file_in = open(filename, 'rb')
        file_out = open(filename + ".out", 'wb')

        bytes_out, crc_out = yenc.encode(file_in, file_out, len(data))

        self.assertEquals(crc, crc_out)


    def testEncodeE(self):
        self._testEncodeFile(BaseTest.FILE_E)


    def testEncodeO(self):
        self._testEncodeFile(BaseTest.FILE_O)


    def _testDecodeFile(self, filename):
        data, crc =  self._readFile(BaseTest.FILE_E)
        file_in = open(BaseTest.FILE_E, 'rb')
        file_out = open(BaseTest.FILE_E + ".out", 'wb')

        bytes_out, crc_out = yenc.encode(file_in, file_out, len(data))

        file_in = open(BaseTest.FILE_E + ".out", 'rb')
        file_out = open(BaseTest.FILE_E + ".dec", 'wb')
        bytes_dec, crc_dec = yenc.decode(file_in, file_out)

        self.assertEquals(crc, crc_dec)

    def testDecodeE(self):
        self._testDecodeFile(BaseTest.FILE_E)

    def testDecodeO(self):
        self._testDecodeFile(BaseTest.FILE_O)


if __name__ == "__main__":
	unittest.main()
