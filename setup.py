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

from distutils.core import setup, Extension

setup(	
	name		= "yenc",
	version		= "0.4",
	author		= "Alessandro Duca",
	author_email	= "alessandro.duca@gmail.com",
	url		= "http://www.golug.it/yenc.html",
	description	= "yEnc Module for Python",
	license		= "LGPL",
	package_dir	= { '': 'lib' },
	py_modules	= ["yenc"],
	ext_modules	= [Extension("_yenc",["src/_yenc.c"],extra_compile_args=["-O2","-g"])]
	)

