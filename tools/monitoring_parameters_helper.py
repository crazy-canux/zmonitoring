#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (C) Canux CHENG <canuxcheng@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Extract Nagios data about applications.
"""

import sys
import os
from pprint import pformat
import logging

# Locate optools settings
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

from apps.nagios.models import Satellite


# Location where to store generated content
VAR_DIR = os.path.join(PROJECT_DIR, 'var')
FILE_NAME = os.path.join(VAR_DIR, '%s.csv')

# Configure basic logger
logger = logging.getLogger('monitoring')
logger.setLevel(logging.INFO)

logger_debug_handler = logging.StreamHandler()
logger_debug_handler.setLevel(logging.DEBUG)

logger_debug_formatter = logging.Formatter('%(message)s')
logger_debug_handler.setFormatter(logger_debug_formatter)

logger.addHandler(logger_debug_handler)

# Define columns and mapping aliases
COLUMN_ORDER = (
    'hostname',
    'address',
    'os',
    'env',
    'location',
    'function',
    'check_timeframe',
    'service',
    'description',
    'expected_results',
    'frequency',
    'retry_frequency',
    'attempts',
    'permissions',
    'procedure',
)

COLUMN_MAPPING = {
    'hostname': 'host_name',
    'address': 'host_address',
    'os': {'host_custom_variables': 'PROC_OS'},
    'env': {'host_custom_variables': 'PROC_ENV'},
    'location': {'host_custom_variables': 'PROC_AREA'},
    'function': 'host_alias',
    'check_timeframe': 'check_period',
    'service': 'description',
    'description': 'notes_expanded',
    'expected_results': 'plugin_output',
    'frequency': 'check_interval',
    'retry_frequency': 'retry_interval',
    'attempts': 'max_check_attempts',
    'permissions': 'contact_groups',
    'procedure': 'notes_url_expanded',
}

# Utility functions
def columns_header(colnames):
    return ";".join(colnames) + "\n"

def data_to_csv(data, columns):
    logger.info(80 * "=")
    logger.info("Processing service \'%s\' on \'%s\'...", data["description"], data["host_name"])
    logger.info(80 * "=")
    logger.debug(pformat(data, indent=4))

    line_options = []

    for colname in columns:
        livecol = COLUMN_MAPPING[colname]
        logger.info("Column mapping %s --> %s", colname, livecol)

        if isinstance(livecol, str):
            if isinstance(data[livecol], list):
                line_options.append(", ".join(data[livecol]))
            else:
                line_options.append(str(data[livecol]))
        elif isinstance(livecol, dict):
            try:
                sub, value = livecol.items().pop()
                line_options.append(str(data[sub][value]))
            except KeyError:
                line_options.append("None")

    logger.info("Parsed options:\n%s", pformat(line_options, indent=4))
    return ";".join(line_options) + "\n"

# Main procedure
if __name__ == '__main__':
    # Satelite connection
    s = Satellite.live_connect()

    # Query some data, just a little ;-)
    service_details = s.query_table_assoc("""GET services
Columns: description host_name host_address host_custom_variables host_alias check_period notes_expanded plugin_output max_check_attempts check_interval retry_interval custom_variables notes_url_expanded contact_groups
Filter: host_groups >= %s
""" % sys.argv[1])

    # Format to CSV
    with open(FILE_NAME % sys.argv[1], 'w') as output:
        output.write(columns_header(COLUMN_ORDER))
        for service in service_details:
            if service.values() == service.keys():
                logger.info("Skipping column header rows.")
                continue
            output.write(data_to_csv(service, COLUMN_ORDER))

