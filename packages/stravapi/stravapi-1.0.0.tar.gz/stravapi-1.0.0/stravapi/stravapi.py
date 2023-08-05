#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: stravapi.py
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
Main code for stravapi

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
import hug
from client import Client
from operator import attrgetter

__author__ = '''Oriol Fabregas <fabregas.oriol@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''01-03-2019'''
__copyright__ = '''Copyright 2019, Oriol Fabregas'''
__credits__ = ["Oriol Fabregas"]
__license__ = '''Apache Software License 2.0'''
__maintainer__ = '''Oriol Fabregas'''
__email__ = '''<fabregas.oriol@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''stravapi'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


client = Client()


@hug.get(examples='activity_type=Ride&number=5')
@hug.local()
def activities(activity_type: hug.types.text, number: hug.types.number):
    """
    Gets the max number of activities sorted by distance

    Args:
        activity_type: string
        number: integer

    Returns: list of dictionaries

    """
    activity_by_type = sorted([activity for activity in client.activities
                               if activity.type == activity_type.capitalize()],
                              key=attrgetter('distance.num'),
                              reverse=True)
    longest_activities = []
    for activity in activity_by_type[:number]:
        _activities = {}
        _activities[activity.name] = activity.distance.num
        longest_activities.append(_activities)
    return longest_activities

