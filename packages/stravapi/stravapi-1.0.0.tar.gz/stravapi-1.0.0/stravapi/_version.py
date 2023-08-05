#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: _version.py
#
# Copyright 2019 Oriol Fabregas
#
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""
Manages the version of the package.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os

__author__ = '''Oriol Fabregas <fabregas.oriol@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''01-03-2019'''
__copyright__ = '''Copyright 2019, Oriol Fabregas'''
__license__ = '''Apache Software License 2.0'''
__maintainer__ = '''Oriol Fabregas'''
__email__ = '''<fabregas.oriol@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

VERSION_FILE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '.VERSION'
    )
)

LOCAL_VERSION_FILE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '.VERSION'
    )
)

try:
    with open(VERSION_FILE_PATH) as f:
        __version__ = f.read()
except IOError:
    with open(LOCAL_VERSION_FILE_PATH) as f:
        __version__ = f.read()
