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

import os
import re
import sys


"""
insert data from nagios and redmine to program database
"""


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

from apps.kpi.models import KpiRedmine, KpiNagios, NagiosNotifications, \
    CountNotifications, RecurrentAlerts, OldestAlerts, RecurrentAlertsWeek, \
    FailedServices, CountFailedServices, CountFailedServicesByApps
from datetime import datetime, timedelta
from django.conf import settings
from django.core import serializers
from django.db.models import Count
from django.utils.timezone import utc
from pickle import dumps
import json
import logging
import nagios
import nagios_notifications
import jobs.redmine



logger = logging.getLogger('jobs.update.kpi')

def insert():
    """
    Execute the requests in the differents databases, then stock the result in the programm database
    """
    number = 0
    notifications_nagios = get_notifications()
    number += insert_nagios_notifications(notifications_nagios)

    one_day = timedelta(days = 1)
    today = datetime.now(tz=utc).replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    yesterday = today - one_day

    # Test if the table KpiNagios of the program is not empty
    if KpiNagios.objects.all().count():
        # Takes the last date foud in the table
        last_date = KpiNagios.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        # set a random date different of yesterday
        last_date = yesterday-one_day

    # If the table has not been updated yesterday
    if last_date != yesterday:
        result_nagios = get_result_nagios()
        number += insert_nagios(result_nagios)

    if CountNotifications.objects.all().count():
        last_date = CountNotifications.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday-one_day

    if last_date != yesterday:
        number += insert_count_notifications()

    if OldestAlerts.objects.all().count():
        last_date = OldestAlerts.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
            minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday

    if last_date != today:
        OldestAlerts.objects.all().delete()
        number += insert_oldest_alerts()

    if KpiRedmine.objects.all().count():
        last_date = KpiRedmine.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday-one_day

    if last_date != yesterday:
       number += insert_redmine()

    if RecurrentAlerts.objects.all().count():
        last_date = RecurrentAlerts.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
            minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday

    if last_date != today:
        RecurrentAlerts.objects.all().delete()
        recurrents_alerts = nagios_notifications.request_recurrent_alerts(31)
        number += insert_recurrent_alerts("RecurrentAlerts", recurrents_alerts)

        RecurrentAlertsWeek.objects.all().delete()
        recurrents_alerts_week = nagios_notifications.request_recurrent_alerts(7)
        number += insert_recurrent_alerts("RecurrentAlertsWeek", recurrents_alerts_week)

    number += insert_count_failed_servicesByApps()

    return "\n %s lignes ajoutees" % number

def get_result_nagios():
    """
    get the results from nagios database
    """
    # return null if a satellite doesn't answer
    result_nagios = nagios.request()
    if not result_nagios:
        raise SystemExit("The connection to a satellite failed")
        # leave the programm by raising an error if a sattelite is "dead"
    return result_nagios
    # return the result if there is no errors

def get_notifications():
    """
    get the last timestamp from the database then use it to get the
    notification from nagios from the last timestamp
    """
    last_timestamp = nagios_notifications.get_last_time()

    notifications_nagios = nagios.request_notifications(last_timestamp)
    return notifications_nagios

def insert_redmine():
    """
    insert redmine kpi into the programm database
    """
    try:
        result_redmine = jobs.redmine.request()
    except:
        logger.exception('Exception occured during fetching of Redmine KPI !')
        raise SystemExit(2)

    number = 0
    for date in result_redmine['requests_opened'].iterkeys():
    # iteraton on the keys to get the differents names in the table
        entree = KpiRedmine()
        entree.date = date
        try:
            last_redmine_kpi = KpiRedmine.objects.latest('date')
            entree.aim_lifetime = last_redmine_kpi.aim_lifetime
        except KpiRedmine.DoesNotExist:
            pass
        entree.requests_opened_external = result_redmine['requests_opened_external'][date]
        entree.requests_closed_external = result_redmine['requests_closed_external'][date]
        entree.requests_remained_external = result_redmine['requests_remained_external'][date]
        entree.requests_waiting_external = result_redmine['requests_waiting_external'][date]
        entree.requests_lifetime_low_external = result_redmine['requests_lifetime_low_external'][date]
        entree.requests_opened = result_redmine['requests_opened'][date]
        entree.requests_closed = result_redmine['requests_closed'][date]
        entree.requests_remained = result_redmine['requests_remained'][date]
        entree.requests_lifetime = result_redmine['requests_lifetime_low'][date]
        entree.requests_lifetime_normal = \
            result_redmine['requests_lifetime_normal'][date]
        entree.requests_lifetime_high  = \
            result_redmine['requests_lifetime_high'][date]
        entree.requests_lifetime_urgent = \
            result_redmine['requests_lifetime_urgent'][date]
        entree.requests_waiting = result_redmine['requests_waiting'][date]
        entree.save()
        number += 1
        print "\r %s kpi redmine saved" % number,
    return number

def insert_nagios_notifications(notifications_nagios):
    """
    insert nagios notifications into the programm database
    """
    number = 0
    for notifications in notifications_nagios:
        entree = NagiosNotifications()
        entree.host = notifications[0]
        entree.service = notifications[1]
        entree.date = datetime.fromtimestamp(notifications[2], tz=utc)
        entree.state = notifications[3]
        # get app
        temp_app=notifications[4]
        regex_app=re.compile("^app_[-a-zA-Z0-9]+$",re.IGNORECASE)
        app = filter(regex_app.search, temp_app)
        #erase 4 char of beginning ("app_")
        if len(app)==0:
            app="NC"
        else:
            app=app[0][4:]
        entree.app= app
        entree.selection_group_host_app=str(notifications[0])+"|"+str(app)
        entree.selection_group_host_service=str(notifications[0])+"|"+str(notifications[1])

        if "ACKNOWLEDGEMENT" in notifications[5]:
            entree.acknowledged = True
        else:
            entree.acknowledged = False
        number += 1
        print "\r %s notifications saved" % number,
        entree.save()
    return number

def insert_nagios(result_nagios):
    """
    insert nagios kpi into the programm database
    """
    number = 0
    one_day = timedelta(days = 1)
    nagios_r = KpiNagios()
    nagios_r.date = datetime.now(tz=utc).replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)-one_day


    # Nagios results ----------------------------------------------------------
    nagios_r.total_host = result_nagios['total_hosts']
    nagios_r.total_services = result_nagios['total_services']
    nagios_r.total_app = result_nagios['total_app']
    nagios_r.written_procedures = result_nagios['written_procedures']
    nagios_r.total_written = result_nagios['total_written']
    nagios_r.missing_procedures = result_nagios['missing_procedures']
    nagios_r.total_missing = result_nagios['total_missing']
    nagios_r.linux = result_nagios['linux']
    nagios_r.windows = result_nagios['windows']
    nagios_r.aix = result_nagios['aix']
    nagios_r.nb_host_down = result_nagios['nb_host_down']

    nagios_r.save()
    number += 1
    print "\n1 kpi nagios saved"
    return number

def insert_count_notifications():
    """
    insert the number of notifications for each state every day
    """
    print "\nCounting Nagios notifications"
    one_day = timedelta(days = 1)
    number = 0
    result = True
    if not CountNotifications.objects.all().count():
        first_date = NagiosNotifications.objects.order_by('date')[0].date
    else:
        first_date = CountNotifications.objects.order_by('-date')[0].date
        first_date += one_day
    first_date = first_date\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    result = nagios_notifications.request(first_date)
    while result:
        notif = CountNotifications()
        notif.date = first_date
        notif.warning = result['warning']
        notif.warning_acknowledged = result['warning_acknowledged']
        notif.critical = result['critical']
        notif.critical_acknowledged = result['critical_acknowledged']
        notif.unknown = result['unknown']
        notif.unknown_acknowledged = result['unknown_acknowledged']
        notif.save()
        first_date += one_day
        number += 1
        print "\r %s kpi notifications count saved" % number,
        result = nagios_notifications.request(first_date)
    return number

def insert_recurrent_alerts(modeleRecurrentAlerts, recurrents_alerts):
    """
    insert all the distincts alerts with the number of times they occured
    """
    print "\nCounting Recurrents alerts"

    number = 0
    for alerts, frequency in recurrents_alerts.items():
        name = str(alerts).split(';')
        if modeleRecurrentAlerts=="RecurrentAlerts":
            recurrent_alert = RecurrentAlerts()
        else:
            recurrent_alert = RecurrentAlertsWeek()
        recurrent_alert.date = frequency[1]
        recurrent_alert.host = name[0]
        recurrent_alert.service = name[1]
        recurrent_alert.frequency = frequency[0]
        recurrent_alert.save()
        number += 1
        print "\r %s Recurrents alerts saved" % number,
    return number

def insert_oldest_alerts():
    """
    insert the oldest alerts active in the database
    """
    print "\nFetching informations for the oldest alerts"
    oldest_alerts = nagios.request_oldest_alerts_hosts()
    date = datetime.now(tz=utc).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    number = 0
    for alert in oldest_alerts:
        old_alert = OldestAlerts()
        old_alert.date = date
        old_alert.host = alert[0]
        old_alert.service = ""
        old_alert.date_error = datetime.fromtimestamp(alert[1], tz=utc)
        old_alert.state = alert[2]
        old_alert.acknowledged = alert[3]
        old_alert.save()
        number += 1
        print "\r %s Oldest alerts saved" % number,
    oldest_alerts = nagios.request_oldest_alerts_services()
    for alert in oldest_alerts:
        old_alert = OldestAlerts()
        old_alert.date = date
        old_alert.host = alert[0]
        old_alert.service = alert[1]
        old_alert.date_error = datetime.fromtimestamp(alert[2], tz=utc)
        old_alert.state = alert[3]
        old_alert.acknowledged = alert[4]
        old_alert.save()
        number += 1
        print "\r %s Oldest alerts saved" % number,
    insert_failed_services()
    insert_count_failed_services()
    return number

def insert_failed_services():
    """
    insert the sum of failed alerts active in the database
    """
    print "\nFetching informations for the failed services"
    #sum warning failed service
    failed_service = FailedServices()
    failed_service.date = datetime.now(tz=utc).replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days=1)
    failed_service.nb_warning = OldestAlerts.objects.filter(state=1).exclude(service="").count()
    failed_service.nb_critical = OldestAlerts.objects.filter(state=2).exclude(service="").count()
    failed_service.nb_unknown = OldestAlerts.objects.filter(state=3).exclude(service="").count()
    failed_service.nb_acknowledged = OldestAlerts.objects.filter(acknowledged=True).exclude(service="").count()
    failed_service.nb_not_acknowledged = OldestAlerts.objects.filter(acknowledged=False).exclude(service="").count()
    failed_service.nb_host_down = OldestAlerts.objects.filter(service="").count()
    nb_day_of_oldest_alert =  datetime.now(tz=utc).replace(hour = 0, minute = 0, second = 0, microsecond = 0) - OldestAlerts.objects.values('date_error').order_by("date_error")[0]['date_error']
    failed_service.nb_oldest_alert = nb_day_of_oldest_alert.days
    failed_service.list_app = OldestAlerts.objects.exclude(service="").count()
    failed_service.nb_failed_by_app = OldestAlerts.objects.exclude(service="").count()
    failed_service.save()

def insert_count_failed_services():
    """
    insert the sum of failed alerts active in the database
    """
    print "\nFetching informations for the count failed services"
    #sum warning failed service
    count_failed_service = CountFailedServices()
    date_now = datetime.now(tz=utc)
    count_failed_service.date = date_now - timedelta(days=1)
    # nb_failed_day
    start_date = date_now
    end_date = date_now - timedelta(days = 1)
    count_failed_service.nb_failed_day = OldestAlerts.objects.filter(date_error__range=(end_date,start_date)).exclude(service="").count()

    # nb_failed_week
    start_date = date_now - timedelta(days = 2)
    end_date = date_now - timedelta(days = 5)
    count_failed_service.nb_failed_week = OldestAlerts.objects.filter(date_error__range=(end_date,start_date)).exclude(service="").count()

    # nb_failed_month
    start_date = date_now - timedelta(days = 6)
    end_date = date_now - timedelta(days = 50)
    count_failed_service.nb_failed_month = OldestAlerts.objects.filter(date_error__range=(end_date,start_date)).exclude(service="").count()

    # nb_failed_some_month
    start_date = date_now - timedelta(days = 51)
    count_failed_service.nb_failed_some_month = OldestAlerts.objects.filter(date_error__lte=start_date).exclude(service="").count()

    count_failed_service.save()

def insert_count_failed_servicesByApps():
    """
    insert the sum of failed alerts  by apps active in the database
    """
    print "\nFetching informations for the count failed services by apps "

    number = 0
    
    if not CountFailedServicesByApps.objects.all().count():
        start_date = NagiosNotifications.objects.order_by('date')[0].date
    else:
        start_date = CountFailedServicesByApps.objects.order_by('-date')[0].date
        start_date = start_date + timedelta(days=1)
    start_date = start_date\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
    now = datetime.now(tz=utc).replace(hour=0,minute=0,second =0,microsecond=0)
    
    while start_date < now:
        period = timedelta(days=1)
        end_date = start_date + period
        data_app = NagiosNotifications.objects.filter(date__range=(start_date,end_date ),acknowledged = 0).values('app').order_by('app').annotate(nb_app=Count('app'))
        nb_total_alert = 0
        tab_temp = []
        list_app = []
        list_all_apps = []
        # check all apps
        list_all_apps_temp = NagiosNotifications.objects.values('app').order_by('app').annotate(nb_app=Count('app'))
        for data_temp in list_all_apps_temp:
            list_all_apps.append(data_temp['app'])
            
        for data in data_app:
            tab_temp.append({'date': start_date.isoformat(), 'nb_app' : data['nb_app'], 'app' : data ['app'] })
            nb_total_alert += data['nb_app']
            list_app.append(data['app'])
        list_app = list(set(list_app))
        list_all_apps = list(set(list_all_apps))
        for data in list_app:
            try:
                list_all_apps.remove(data)
            except: pass
        for data_temp in list_all_apps:
            tab_temp.append({'date':start_date.isoformat(),'nb_app': 0, 'app':data_temp})
            
        tab_temp.append({'date':start_date.isoformat(),'nb_app': nb_total_alert, 'app':u"Total Alerts"})
        failed_service_by_apps = CountFailedServicesByApps()
        failed_service_by_apps.date= start_date 
        failed_service_by_apps.list_app_graph_data = json.dumps(tab_temp)
        failed_service_by_apps.save()
        start_date = end_date
        number += 1
    return number


if __name__ == '__main__':
    print(insert())
