#!/usr/bin/env python
# -*- coding: utf-8 -*-
##=============================================================================
 #
 # Copyright (C) 2003, 2011 Alessandro Duca <alessandro.duca@gmail.com>
 #
 # This library is free software; you can redistribute it and/or
 # modify it under the terms of the GNU Lesser General Public
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

import sys
import os
import os.path
import yenc
import getopt
from stat import *
from binascii import crc32

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:")
    except getopt.GetoptError:
        usage()
    file_out = sys.stdout
    for o,a in opts:
        if o == '-o':
            file_out = open(a,"wb")
    if file_out is sys.stdout:
        sys.stdout = None
    with file_out:
        if args:
            filename = args[0]
            if os.access( filename, os.F_OK | os.R_OK ):
                file_in = open(filename,"rb")
            else:
                sys.stderr.write("couldn't access %s\n" % filename)
                sys.exit(2)
        else:
            usage()
        with file_in:
            with open(filename,"rb") as file:
                crc = "%08x"%(0xFFFFFFFF & crc32(file.read())) 
            name = os.path.split(filename)[1]
            size = os.stat(filename)[ST_SIZE]
            file_out.write("=ybegin line=128 size=%d crc32=%s name=%s\r\n" % (size, crc, name) )
            try:
                encoded, crc_out = yenc.encode(file_in, file_out, size)
            except Exception, e:
                sys.stderr.write("{}\n".format(e))
                sys.exit(3)
        file_out.write("=yend size=%d crc32=%s\r\n" % (encoded, crc_out))

def usage():
    sys.stderr.write("Usage: yencode.py <-o outfile> filename\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
