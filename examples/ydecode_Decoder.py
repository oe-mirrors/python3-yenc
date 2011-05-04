#!/usr/bin/env python
## -*- coding: utf-8 -*-
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

import os
import sys
import re

import yenc

NAME_RE 	= re.compile(r"^.*? name=(.+?)\r\n$")
LINE_RE 	= re.compile(r"^.*? line=(\d{3}) .*$")
SIZE_RE 	= re.compile(r"^.*? size=(\d+) .*$")
CRC32_RE	= re.compile(r"^.*? crc32=(\w+)")

def main():
	head_crc = trail_crc = ""
	if len(sys.argv) > 1:
		file_in = open(sys.argv[1],"rb")
	else:
		file_in	= sys.stdin
	while 1:
		line = file_in.readline()
		if line.startswith("=ybegin "):
			try:
				name, size = NAME_RE.match(line).group(1), int(SIZE_RE.match(line).group(1))
				m_obj = CRC32_RE.match(line)
				if m_obj:
					head_crc = m_obj.group(1)
			except re.error, e:
				sys.stderr.write("err-critical: malformed =ybegin header\n")
				sys.exit(1)
			break
		elif not line:
			sys.stderr.write("err-critical: no valid =ybegin header found\n")
			sys.exit(1)
	file_out = open(name,"wb")
	dec = yenc.Decoder(file_out)
	trailer = ""
	garbage = 0
	while True:
		data = file_in.readline()
		if data.startswith("=yend"):
			trailer = data
			break
		elif dec.getSize() >= size:
			garbage = 1
		else:
			dec.feed(data)
			dec.flush()
	if trailer:
		try:	
			size = int(SIZE_RE.match(trailer).group(1))
			m_obj = CRC32_RE.search(trailer)
			if m_obj:
				trail_crc = m_obj.group(1)
		except re.error, e:
			sys.stderr.write("err: malformed =yend trailer\n")
	else:
		sys.stderr.write("warning: couldn't find =yend trailer\n")
	if garbage:
		sys.stderr.write("warning: garbage before =yend trailer\n")
	if head_crc:
		tmp_crc = head_crc.lower()
	elif trail_crc:
		tmp_crc = trail_crc.lower()
	else:
		sys.exit(0)
#	print "comparing"
	if cmp(tmp_crc, dec.getCrc32()):
		sys.stderr.write("err: header: %s dec: %s CRC32 mismatch\n" % (tmp_crc,dec.getCrc32()) )
		sys.exit(1)
	else:
		sys.exit(0)

if __name__ == "__main__":
	main()
