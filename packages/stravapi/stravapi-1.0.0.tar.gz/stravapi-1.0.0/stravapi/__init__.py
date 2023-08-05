#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: __init__.py
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
stravapi package

Import all parts from stravapi here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .client import Client

__author__ = '''Oriol Fabregas <fabregas.oriol@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''01-03-2019'''
__copyright__ = '''Copyright 2019, Oriol Fabregas'''
__license__ = '''Apache Software License 2.0'''
__maintainer__ = '''Oriol Fabregas'''
__email__ = '''<fabregas.oriol@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is to 'use' the module(s), so lint doesn't complain
assert __version__
assert client
