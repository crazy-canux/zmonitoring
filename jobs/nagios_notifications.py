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
get the notifications from nagios results
"""

import calendar
from datetime import datetime, timedelta
from django.utils.timezone import utc
from apps.kpi.models import NagiosNotifications


def get_last_time():
    """
    return the last timestamp foud in the database
    return 0 if the database is empty
    """
    try:
        last_date = NagiosNotifications.objects.order_by('-date')[0].date
        last_timestamp = calendar.timegm(last_date.timetuple())
    except:
        last_timestamp = 0

    return last_timestamp

def request(date):
    """
    return a dictionnary containing the number of alerts for each state
    """
    one_day = timedelta(days = 1)
    date = date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    late = date + one_day
    now = datetime.now(tz=utc)\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    if date >= now:
        return False
    else:
        result = NagiosNotifications.objects.filter(date__gte = date,
            date__lt = late)
        warning = result.filter(
            state = 1, acknowledged = False).count()
        warning_acknowledged = result.filter(
            state = 1, acknowledged = True).count()
        critical = result.filter(
            state = 2, acknowledged = False).count()
        critical_acknowledged = result.filter(
            state = 2, acknowledged = True).count()
        unknown = result.filter(
            state = 3, acknowledged = False).count()
        unknown_acknowledged = result.filter(
            state = 3, acknowledged = True).count()
        result = {
        'warning': warning,
        'warning_acknowledged': warning_acknowledged,
        'critical': critical,
        'critical_acknowledged': critical_acknowledged,
        'unknown': unknown,
        'unknown_acknowledged': unknown_acknowledged 
        }
        return result

def request_recurrent_alerts(nb_days):
    """
    return a dictionnary containing the number of each alerts per numbers dayssql
    """
    today = datetime.now(tz=utc)\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    period = timedelta(days = nb_days)
    first_date = today - period
    alerts = NagiosNotifications.objects\
        .filter(date__gte = first_date, date__lt = today)\
        .filter(acknowledged = 0)\
        .values('host', 'service','date')
    alerts_list = list(alerts)
#    for index, alert in enumerate(alerts_list):
#        if not alert['host'] in hosts:
#            del alerts_list[index]
    count = {}
    frequency=0
    for alert in alerts_list:
        name = "%s;%s" % (alert["host"], alert["service"])
        if count.has_key(str(name)):
            frequency =  count[str(name)][0] + 1
            if alert["date"]>count[str(name)][1]:
                data = [frequency, alert["date"]]
            else:
                data = [frequency, count[str(name)][1]]
        else:
            frequency = 1
            data = [frequency, alert["date"]]
        count[str(name)]=data
    
    return count
