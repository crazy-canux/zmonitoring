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
get the redmine kpi from redmine
"""

from apps.kpi.models import KpiRedmine
from datetime import datetime, timedelta
from django.utils.timezone import utc
from sqlalchemy import *
import logging

from database import redmine


logger = logging.getLogger(__name__)

def request():
    """
    return the key indicators from redmine database
    """
    # Establish Redmine database connection
    redmine_db_connection = redmine.engine.connect()

    # count the number of entry in the program database for the Redmine kpi
    number = KpiRedmine.objects.count()

    requests_opened = {}
    requests_opened_external = {}
    requests_closed = {}
    requests_closed_external = {}
    requests_remained = {}
    requests_remained_external = {}
    requests_lifetime_low = {}
    requests_lifetime_low_external = {}
    requests_lifetime_normal = {}
    requests_lifetime_high = {}
    requests_lifetime_urgent = {}
    requests_waiting = {}
    requests_waiting_external = {}
    one_day = timedelta(days = 1)

    # Which time it is ?
    today = datetime.now(tz=utc)
    today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # first execution of the script
    if not number:
        day_midnight = redmine.issues.order_by(redmine.Issues.created_on.desc()).first().created_on
        day_midnight -= one_day
    else:
        day_midnight = KpiRedmine.objects.order_by('-date')[0].date
        day_midnight += one_day


    day_midnight = day_midnight.replace(
        hour = 0, minute = 0, second = 0, microsecond = 0, tzinfo = utc)
    processing_day = day_midnight + one_day

    logger.info('Updating Redmine KPI from date: %s', day_midnight)

    while processing_day <= today:
        # loop that goes throuh all the database day per day
        #
        logger.info('Processing request for day %s.', processing_day)

        # Opened requests
        logger.info('Fetching new opened requests...')
        # Convert to date to fix this:
        #   Warning: Incorrect datetime value: '2013-03-18 00:00:00.000001+00:00' for column 'created_on' at row 1
        opened_requests = redmine.issues.join(redmine.Projects).filter(
            redmine.Issues.created_on >= day_midnight.date(),
            redmine.Issues.created_on < processing_day.date(),
            redmine.Projects.identifier != 'orion',
        )
        opened_external_requests = redmine.issues.join(redmine.Projects, redmine.CustomValues).filter(
            redmine.Issues.created_on >= day_midnight.date(),
            redmine.Issues.created_on < processing_day.date(),
            redmine.Projects.identifier != 'orion', redmine.CustomValues.value=='External'
        )
        
        requests_opened[str(day_midnight)] = opened_requests.count()
        requests_opened_external[str(day_midnight)] = opened_external_requests.count()
        logger.debug('SQL query fetching new opened request:')
        logger.debug('%s', opened_requests)

        for request in opened_requests:
            logger.debug('[New request] #%s: %s, created: %s', request.id, request.subject, request.created_on)

        # Closed requests (id: 12 Delivery)
        logger.info('Fetching closed requests...')
        requests_closed[str(day_midnight)] = redmine.issues.join(redmine.Projects, redmine.IssueStatus).filter(
            redmine.Issues.due_date == day_midnight.date(),
            or_(redmine.IssueStatus.is_closed == True, redmine.IssueStatus.id == 12),
            redmine.Projects.identifier != 'orion',
        ).count()
        
        requests_closed_external[str(day_midnight)] = redmine.issues.join(redmine.Projects, redmine.IssueStatus, redmine.CustomValues).filter(
            redmine.Issues.due_date == day_midnight.date(),
            or_(redmine.IssueStatus.is_closed == True, redmine.IssueStatus.id == 12),
            redmine.Projects.identifier != 'orion', redmine.CustomValues.value=='External'
        ).count()

        avg = timedelta(days = 30)
        lifetime_low = timedelta()
        lifetime_normal = timedelta()
        lifetime_high = timedelta()
        lifetime_urgent = timedelta()
        n_low = 0
        n_normal = 0
        n_high = 0
        n_urgent = 0

        # Remained requests
        logger.info('Fetching remaining requests...')
        requests_remained[str(day_midnight)] = redmine.issues.join(redmine.Projects, redmine.IssueStatus).filter(
            redmine.Issues.created_on < processing_day,
            or_(redmine.Issues.due_date > day_midnight.date(), and_( redmine.IssueStatus.is_closed == False, redmine.IssueStatus.id != 12)),
            redmine.Projects.identifier != 'orion',
        ).count()
        
        requests_remained_external[str(day_midnight)] = redmine.issues.join(redmine.Projects,
                                                                            redmine.IssueStatus,
                                                                            redmine.CustomValues).filter(
            redmine.Issues.created_on < processing_day,
            or_(redmine.Issues.due_date > day_midnight.date(), and_( redmine.IssueStatus.is_closed == False, redmine.IssueStatus.id != 12)),
            redmine.Projects.identifier != 'orion', redmine.CustomValues.value=='External'
        ).count()

        # Lifetime
        logger.info('Compute request lifetime...')
        for request in redmine.issues.join(redmine.Projects, redmine.IssueStatus).filter(
            redmine.Issues.due_date > (day_midnight-avg).date(),
            redmine.Issues.due_date < day_midnight.date(),
            redmine.Projects.identifier != 'orion',
            or_(redmine.IssueStatus.name == 'Closed', redmine.IssueStatus.id == 12)):
            created_on = request.created_on.date()
            due_date = request.due_date
            priority = request.priority_id
            lifetime = timedelta(days = calcul_days(due_date, created_on))

            if priority == 20:
                lifetime_low += lifetime
                n_low += 1
            elif priority == 4:
                lifetime_normal += lifetime
                n_normal += 1
            elif priority == 5:
                lifetime_high += lifetime
                n_high += 1
            elif priority == 6:
                lifetime_urgent += lifetime
                n_urgent += 1

        if n_low > 0:
            requests_lifetime_low[str(day_midnight)] = (lifetime_low.total_seconds() / n_low)
        else:
            requests_lifetime_low[str(day_midnight)] = 0

        if n_normal > 0:
            requests_lifetime_normal[str(day_midnight)] = (lifetime_normal.total_seconds() / n_normal)
        else:
            requests_lifetime_normal[str(day_midnight)] = 0

        if n_high > 0:
            requests_lifetime_high[str(day_midnight)] = (lifetime_high.total_seconds() / n_high)
        else:
            requests_lifetime_high[str(day_midnight)] = 0

        if n_urgent > 0:
            requests_lifetime_urgent[str(day_midnight)] = (lifetime_urgent.total_seconds() / n_urgent)
        else:
            requests_lifetime_urgent[str(day_midnight)] = 0

        # Global lifetime
        if n_normal + n_high + n_urgent + n_low != 0:
            requests_lifetime_low[str(day_midnight)] = (lifetime_normal.total_seconds()
                                                        + lifetime_high.total_seconds()
                                                        + lifetime_urgent.total_seconds()
                                                        + lifetime_low.total_seconds()) / (n_normal + n_high + n_urgent + n_low)
        lifetime_low_external = timedelta()
        n_low_external = 0
        
        for request in redmine.issues.join(redmine.Projects, redmine.IssueStatus, redmine.CustomValues).filter(
            redmine.Issues.due_date > (day_midnight-avg).date(),
            redmine.Issues.due_date < day_midnight.date(),
            redmine.Projects.identifier != 'orion',
            redmine.CustomValues.value=='External',
            or_(redmine.IssueStatus.name == 'Closed', redmine.IssueStatus.id == 12)):
            created_on = request.created_on.date()
            due_date = request.due_date
            priority = request.priority_id
            lifetime = timedelta(days = calcul_days(due_date, created_on))
            lifetime_low_external += lifetime
            n_low_external += 1
        
        # Global lifetime
        if n_low_external != 0:
            requests_lifetime_low_external[str(day_midnight)] = (lifetime_low_external.total_seconds()) / (n_low_external)

        logger.info('Fetching Waiting requests...')
        if processing_day == today:
            requests_waiting[str(day_midnight)] = redmine.issues.join(redmine.Projects, redmine.IssueStatus).filter(
                redmine.Projects.identifier != 'orion',
                or_(redmine.IssueStatus.name == 'Awaiting requestor', redmine.IssueStatus.name == 'Feedback'),
            ).count()
            requests_waiting_external[str(day_midnight)] = redmine.issues.join(redmine.Projects, redmine.IssueStatus, redmine.CustomValues).filter(
                redmine.Projects.identifier != 'orion', redmine.CustomValues.value=='External',
                or_(redmine.IssueStatus.name == 'Awaiting requestor', redmine.IssueStatus.name == 'Feedback'),
            ).count()
        else:
            requests_waiting[str(day_midnight)] = 0

        day_midnight += one_day
        processing_day += one_day

    redmine_db_connection.close()

    results = {
        'requests_opened': requests_opened,
        'requests_opened_external': requests_opened_external,
        'requests_closed': requests_closed,
        'requests_closed_external': requests_closed_external,
        'requests_remained': requests_remained,
        'requests_remained_external': requests_remained_external,
        'requests_lifetime_low_external': requests_lifetime_low_external,
        'requests_lifetime_low': requests_lifetime_low,
        'requests_lifetime_normal': requests_lifetime_normal,
        'requests_lifetime_high': requests_lifetime_high,
        'requests_lifetime_urgent': requests_lifetime_urgent,
        'requests_waiting': requests_waiting,
        'requests_waiting_external': requests_waiting_external
    }
    return results

def calcul_days(today, date_request):
    """
    calcul the number of days between two dates without the weekends
    """
    num = 0
    one_day = timedelta(days = 1)
    while date_request <  today:
        if date_request.weekday() != 5 and date_request.weekday() != 6:
            num += 1
        date_request += one_day
    return num
