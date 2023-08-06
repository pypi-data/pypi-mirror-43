#!/usr/bin/env python
# -*- coding: utf8 -*-
# library for communicating with an isc dhcp server over the omapi protocol
#
# Copyright 2010-2017 Cygnus Networks GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import distutils.core

distutils.core.setup(name='pypureomapi',
	version='0.8',
	description="ISC DHCP OMAPI protocol implementation in Python",
	long_description="This module provides a OMAPI implementation for managing ISC DHCP server by OMAPI protocol purely in Python code. You can query, create or modify ISC DHCP leases with this module. This module grew out of frustration about pyomapi and later pyomapic, which use swig and the static library provided with ISC DHCP without proper error handling. pypureomapi fixes these issues and can be used more or less as a drop-in replacement for pyomapic.",
	author='Helmut Grohne',
	author_email='h.grohne@cygnusnetworks.de',
	maintainer='Dr. Torge Szczepanek',
	maintainer_email='debian@cygnusnetworks.de',
	license='Apache-2.0',
	url='https://github.com/CygnusNetworks/pypureomapi',
	py_modules=['pypureomapi'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: System Administrators",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Topic :: Internet",
		"Topic :: System :: Networking",
		"Topic :: Software Development :: Libraries :: Python Modules",
	]
)
