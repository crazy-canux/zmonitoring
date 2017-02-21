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
from apps.nagios.models import Satellite
from django.conf import settings
from os import path
import os
import re

"""
get the results from nagios
"""



SATELLITES = Satellite.live_connect()

def request():
    """
    get the kpi from redmine
    """
    kbpath = "/var/www/kb/data/pages" if not settings.DEBUG else os.path.join(settings.PROJECT_PATH, 'var/pages')

    if not SATELLITES:
        return False

    print "Fetching informations for the kpi nagios"

    # Total number of hosts ---------------------------------------------------

    nb_total_hosts = SATELLITES.query("""\
GET hosts
Stats: name != \" \"
""")
    nombre = 0
    for sat in nb_total_hosts:
        nombre += sat[0]

    nb_total_hosts = nombre
    
    # nb_host_down
    
    nb_host_down_temp = SATELLITES.query("""\
GET hosts
Columns: name last_hard_state_change state acknowledged
Filter: hard_state = 1
Filter: notifications_enabled = 1
Filter: scheduled_downtime_depth = 0
Filter: state > 0
""")
    nb_host_down = len(nb_host_down_temp)

    # Total number of services ------------------------------------------------

    nb_total_services = SATELLITES.query("""\
GET services
Stats: description != \" \"
""")
    nombre = 0
    for sat in nb_total_services:
        nombre += sat[0]

    nb_total_services = nombre
    
    # Total of alerts
    
    nb_total_app_temp = SATELLITES.query_column_unique("""\
GET hostgroups
Columns: name
""")
    
    csv_report_dir = "/home/django/public_html/reporting" if not settings.DEBUG else "/tmp"
    report_app = open(path.join(csv_report_dir, "list_apps.csv"), "w")
    report_app.write("Apps;\n")
    regex_app=re.compile("^app_[-a-zA-Z0-9]+$",re.IGNORECASE)
    app = filter(regex_app.search, nb_total_app_temp)
    nb_total_app = len(app) 
    
            
    for app_name in app:        
        report_app.write("%s;\n" % app_name)
    report_app.close()



    # Total number of Linux ---------------------------------------------------

    nb_linux = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_linux
""")
    nombre = 0
    for sat in nb_linux:
        nombre += sat[0]

    nb_linux = nombre


    # Total number of Windows -------------------------------------------------

    nb_windows = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_windows
""")
    nombre = 0
    for sat in nb_windows:
        nombre += sat[0]

    nb_windows = nombre


    # Total number of AIX -----------------------------------------------------

    nb_aix = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_aix
""")
    nombre = 0
    for sat in nb_aix:
        nombre += sat[0]

    nb_aix = nombre

    # get the service with path to the procedure ------------------------------

    services_all = SATELLITES.query("""\
GET services
Columns: host_name description notes_url_expanded contact_groups
""")
    written_procedures = 0
    missing_procedures = 0
    total_written = 0
    total_missing = 0

    csv_report_dir = "/home/django/public_html/reporting" if not settings.DEBUG else "/tmp"

    myreport = open(path.join(csv_report_dir, "detailled_report.csv"), "w")
    my_simple_report = open(path.join(csv_report_dir, "simple_report.csv"), "w")
    myreport.write("written;hostname;services;procedure;stratos\n")
    my_simple_report.write("written;procedure;\n")
    procedures = {}
    for services in services_all:
        procedure_path = services[2].split('/')[-1].strip(':').replace(':', '/').lower()
        empty = 1
        for serv in services[3]:
            if empty == 1:
                list_contact = "%s" % serv
                empty = 0
            else:
                list_contact += ", %s" % serv
                empty = 0
        if path.lexists("%s/%s.txt" % (kbpath, procedure_path)):
            total_written +=1
            myreport.write("yes;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 1
        else:
            total_missing += 1
            myreport.write("no;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 0
    for procedure, written in procedures.items():
        if written:
            my_simple_report.write("yes;%s\n" % procedure)
            written_procedures += 1
        else:
            my_simple_report.write("no;%s\n" % procedure)
            missing_procedures += 1
    myreport.close()

    result = {
    'total_hosts': nb_total_hosts,
    'total_services': nb_total_services,
    'total_app' : nb_total_app,
    'linux': nb_linux,
    'windows': nb_windows,
    'aix': nb_aix,
    'written_procedures': written_procedures,
    'missing_procedures': missing_procedures,
    'total_written' : total_written,
    'total_missing' : total_missing,
    'nb_host_down' : nb_host_down
    }

    return result

def request_notifications(last_timestamp):
    """
    get the notifications from nagios
    """
    print "Fetching informations for the nagios notifications"
    # Get ALL the notifications from the last timestamp -----------------------

    notifications_satellites = SATELLITES.query("""\
GET log
Columns: host_name service_description time state current_host_groups options 
Filter: class = 3
Filter: time > %s
Filter: command_name ~ email
Filter: options !~ ACKNOWLEDGEMENT
Filter: state = 1
And: 2
Filter: options !~ ACKNOWLEDGEMENT
Filter: state = 2
And: 2
Filter: options !~ ACKNOWLEDGEMENT
Filter: state = 3
And: 2
Filter: options ~ ACKNOWLEDGEMENT
Filter: state = 1
And: 2
Filter: options ~ ACKNOWLEDGEMENT
Filter: state = 2
And: 2
Filter: options ~ ACKNOWLEDGEMENT
Filter: state = 3
And: 2
Or: 6
""" % last_timestamp)

    return notifications_satellites

def request_oldest_alerts_hosts():
    """
    return a dictionnary containing the oldest active alerts
    """
    oldest_alerts = SATELLITES.query("""\
GET hosts
Columns: name last_hard_state_change state acknowledged
Filter: hard_state = 1
Filter: notifications_enabled = 1
Filter: scheduled_downtime_depth = 0
Filter: state > 0
""")
    return oldest_alerts

def request_oldest_alerts_services():
    """
    return a dictionnary containing the oldest active alerts 
    """
    oldest_alerts = SATELLITES.query("""\
GET services
Columns: host_name description last_hard_state_change state acknowledged 
Filter: state_type = 1
Filter: notifications_enabled = 1
Filter: state > 0
Filter: scheduled_downtime_depth = 1
Filter: host_scheduled_downtime_depth = 1
Or: 2
Negate:
""")
    return oldest_alerts







