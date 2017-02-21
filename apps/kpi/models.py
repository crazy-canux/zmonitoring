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
django models
"""
from django.db import models
from datetime import timedelta


class KpiNagios(models.Model):
    """
    Stock all the key indicators found in Nagios Database
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null=True)

    total_host = models.PositiveIntegerField('Hosts')
    total_services = models.PositiveIntegerField('Services')
    total_app = models.PositiveIntegerField('Apps',default=0)
    written_procedures = models.PositiveIntegerField('written proc')
    missing_procedures = models.PositiveIntegerField('missing proc')
    linux = models.PositiveIntegerField()
    windows = models.PositiveIntegerField()
    aix = models.PositiveIntegerField()
    comment_host = models.TextField(blank=True, default="")
    comment_procedure = models.TextField('comment proc', blank=True, default="")
    total_written = models.PositiveIntegerField()
    total_missing = models.PositiveIntegerField()
    comment_service = models.TextField('comment serv', blank=True, default="")
    nb_host_down = models.PositiveIntegerField()
    
    def __unicode__(self):
        return str(self.date)

class KpiRedmine(models.Model):
    """
    Stock all the key indicators found in Redmine Database
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null=True)

    requests_opened = models.PositiveIntegerField('opened')
    requests_opened_external = models.PositiveIntegerField('opened_external', null=True)
    requests_closed = models.PositiveIntegerField('closed')
    requests_closed_external = models.PositiveIntegerField('closed_external', null=True)
    requests_remained = models.PositiveIntegerField('remained')
    requests_remained_external = models.PositiveIntegerField('remained_external', null=True)
    requests_lifetime = models.PositiveIntegerField()
    requests_lifetime_low_external = models.PositiveIntegerField('lifetime_low_external', null=True)
    requests_lifetime_normal = models.PositiveIntegerField()
    requests_lifetime_high = models.PositiveIntegerField()
    requests_lifetime_urgent = models.PositiveIntegerField()
    comment_lifetime = models.TextField(blank=True, default="")
    requests_waiting = models.PositiveIntegerField('waiting', null=True)
    requests_waiting_external = models.PositiveIntegerField('waiting_external', null=True)
    aim_lifetime = models.PositiveIntegerField(help_text='Aim from the boss', default=5*24*60*60)

    def lifetime(self):
        """
        return the lifetime global
        """
        return "%s" % timedelta(seconds = self.requests_lifetime)

    def lifetime_normal(self):
        """
        return the lifetime normal
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_normal)

    def lifetime_high(self):
        """
        return the lifetime high
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_high)

    def lifetime_urgent(self):
        """
        return the lifetime urgent
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_urgent)

    def lifetime_aim(self):
        """
        return the lifetime aim
        """
        return "%s" % timedelta(seconds = self.aim_lifetime)


    lifetime.admin_order_field = 'requests_lifetime'
    lifetime.short_description = 'lifetime (global)'

    lifetime_normal.admin_order_field = 'requests_lifetime_normal'
    lifetime_normal.short_description = 'lifetime (normal)'

    lifetime_high.admin_order_field = 'requests_lifetime_high'
    lifetime_high.short_description = 'lifetime (high)'

    lifetime_urgent.admin_order_field = 'requests_lifetime_urgent'
    lifetime_urgent.short_description = 'lifetime (urgent)'

    lifetime_aim.admin_order_field = 'aim_lifetime'
    lifetime_aim.short_description = 'Aim lifetime'

    def __unicode__(self):
        return str(self.date)

class NagiosNotifications(models.Model):
    """
    Stock all the key indicators found in the table log of Nagios Database
    """
    class Meta:
        ordering = ["date"]
    
    host = models.CharField(max_length = 64)
    service = models.CharField(max_length = 128, null = True, blank=True)
    app= models.CharField(max_length = 250, null = True, blank=True)
    selection_group_host_service=models.CharField(max_length = 250, null = True, blank=True,db_index=True)
    selection_group_host_app=models.CharField(max_length = 250, null = True, blank=True,db_index=True)
    date = models.DateTimeField(blank=True)
    STATE_CHOICES = ((1, 'Warning'),(2, 'Critical'),(3,'Unknown'))
    state = models.PositiveIntegerField(choices = STATE_CHOICES)
    acknowledged = models.BooleanField()

    def __unicode__(self):
        return str(self.date)
    
    def to_dict(self):
        return {"date": self.date, "app": self.app}

class CountNotifications(models.Model):
    """
    Count the notifications group by date, state, and acknowledged
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null = True)
    warning = models.PositiveIntegerField()
    warning_acknowledged = models.PositiveIntegerField()
    critical = models.PositiveIntegerField()
    critical_acknowledged = models.PositiveIntegerField()
    unknown = models.PositiveIntegerField()
    unknown_acknowledged = models.PositiveIntegerField()
    comment_notification_warning = models.TextField('comment warning', blank=True, default="")
    comment_notification_warning_ack = models.TextField('comment warning ack', blank=True, default="")
    comment_notification_critical = models.TextField('comment critical', blank=True, default="")
    comment_notification_critical_ack = models.TextField('comment critical ack', blank=True, default="")
    comment_notification_unknown = models.TextField('comment unknown', blank=True, default="")
    comment_notification_unknown_ack = models.TextField('comment unknown ack', blank=True, default="")

    def __unicode__(self):
        return str(self.date)

class RecurrentAlerts(models.Model):
    """
    Stock the recurrent alerts for the last 31 days
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null = True)
    host = models.CharField(max_length = 64)
    service = models.CharField(max_length = 128, null = True, blank=True)
    frequency = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.date)
    
class RecurrentAlertsWeek(models.Model):
    """
    Stock the recurrent alerts for the last 7 days
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null = True)
    host = models.CharField(max_length = 64)
    service = models.CharField(max_length = 128, null = True, blank=True)
    frequency = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.date)

class OldestAlerts(models.Model):
    """
    Stock the oldest active alerts
    """
    class Meta:
        ordering = ["date"]

    date = models.DateTimeField(null = True)
    host = models.CharField(max_length = 64)
    service = models.CharField(max_length = 128, null = True, blank=True)
    date_error = models.DateTimeField(null = True, blank=True)
    STATE_CHOICES = ((1, 'Warning'),(2, 'Critical'),(3,'Unknown'))
    state = models.PositiveIntegerField(choices = STATE_CHOICES)
    acknowledged = models.BooleanField()
    def __unicode__(self):
        return str(self.date)
    
class FailedServices(models.Model):
    """
    Stock the sum of failed services by categories active alerts
    """

    date = models.DateTimeField(null = True)
    nb_warning = models.PositiveIntegerField()
    nb_critical = models.PositiveIntegerField()
    nb_unknown = models.PositiveIntegerField()
    nb_acknowledged = models.PositiveIntegerField()
    nb_not_acknowledged = models.PositiveIntegerField()
    nb_host_down = models.PositiveIntegerField()
    nb_oldest_alert = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.date)
    
class CountFailedServicesByApps(models.Model):
    """
    Stock the sum of failed services by apps active alerts
    """
    date = models.DateTimeField(null = True)
    list_app_graph_data = models.TextField()
    
    
    
class CountFailedServices(models.Model):
    """
    Stock the sum of failed services by categories active alerts
    """

    date = models.DateTimeField(null = True)
    nb_failed_day = models.PositiveIntegerField()
    nb_failed_week = models.PositiveIntegerField()
    nb_failed_month = models.PositiveIntegerField()
    nb_failed_some_month = models.PositiveIntegerField()
    
    def __unicode__(self):
        return str(self.date)

