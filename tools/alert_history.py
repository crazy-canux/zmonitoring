#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
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
Show a nice alert history exportable as CSV.
"""

from __future__ import print_function

import sys
import os
import argparse
from datetime import datetime
import time
from pprint import pformat
import pytz
import logging

# Locate optools settings
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

from apps.nagios.models import Satellite


# Configure basic logger
logger = logging.getLogger('monitoring')
logger.setLevel(logging.INFO)

logger_debug_handler = logging.StreamHandler()
logger_debug_handler.setLevel(logging.DEBUG)

logger_debug_formatter = logging.Formatter('%(message)s')
logger_debug_handler.setFormatter(logger_debug_formatter)

logger.addHandler(logger_debug_handler)

# Argument types
def timestamp(datestr):
    fmt = "%d-%m-%Y"
    d = datetime.strptime(datestr, fmt)
    return time.mktime(d.timetuple())

# Mapping of Nagios states with human name
STATES = {
    0: "OK",
    1: "WARNING",
    2: "CRITICAL",
    3: "UNKNOWN"
}


# Show the following columns in report
show_columns = [
    "time",
    "type",
    "state",
    "state_type",
    "host_name",
    "service_description",
    "plugin_output",
]

# Main procedure
if __name__ == '__main__':
    started_time = datetime.now()

    # Define script args
    args_parser = argparse.ArgumentParser(
        description="Export alert and notification history for a hostgroup.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args_parser.add_argument('--columns',
                             dest="show_columns",
                             metavar="COL_NAME",
                             nargs='*',
                             default=show_columns,
                             help='Livestatus columns from log table that should be shown in the report.')

    args_parser.add_argument('--start',
                             dest="start_period",
                             metavar="DD-MM-YYY",
                             type=timestamp,
                             help='Start period of the report.',
                             required=True)

    args_parser.add_argument('--end',
                             dest="end_period",
                             metavar="DD-MM-YYY",
                             type=timestamp,
                             help='End period of the report.',
                             required=True)

    args_parser.add_argument('--group',
                             dest="group",
                             metavar="HOSTGROUP",
                             help='Limit search to host group name.',
                             required=True)

    args_parser.add_argument('output',
                             type=argparse.FileType('w'),
                             help="Output CSV file name.")

    args_parser.add_argument('--debug',
                             dest="debug",
                             action="store_true",
                             help="Enable debug details.")

    args = args_parser.parse_args()

    # Should we show debug info ?
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.info("Starting at {}.".format(started_time))

    logger.debug("Arguments passed to command line:")
    logger.debug(pformat(vars(args)))

    # Satelite connection
    logger.info("Establishing communication to Nagios Satellites...")
    s = Satellite.live_connect()

    # Query some data, just a little ;-)
    logger.info("Querying log table...")
    query_results = s.query_table("""GET log
Filter: class = 1
Filter: class = 3
Or: 2
Filter: state != 3
Filter: time >= %d
Filter: time <= %d
Filter: current_host_groups >= %s
And: 5
Columns: %s
""" % (args.start_period, args.end_period, args.group," ".join(args.show_columns)))

    # Sort by timestamp ascending
    logger.info("Sorting results by timestamp...")
    query_results = sorted(query_results, key=lambda result: result[0])

    # Show results
    logger.info("Processing results...")
    args.output.write("{}\n".format(";".join(args.show_columns)))
    for line in query_results:
        line[0] = datetime.fromtimestamp(line[0], tz=pytz.utc).strftime('%d-%m-%Y %H:%M:%S %Z')
        line[2] = STATES[line[2]]

        args.output.write("{}\n".format(";".join(line)))

    logger.info("Done in {}.".format(datetime.now() - started_time))
