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
from apps.kpi.models import RecurrentAlertsWeek
from django.contrib import admin
from django.utils import timezone
from models import KpiNagios, KpiRedmine, NagiosNotifications, \
    CountNotifications, RecurrentAlerts, OldestAlerts, FailedServices, CountFailedServices, CountFailedServicesByApps
import pytz

"""
settings from the admin site
"""


class KpiNagiosAdmin(admin.ModelAdmin):
    """
    modify default settings for kpi nagios
    """
    #fields = (('date', 'total_host', 'total_services', 'written_procedures',
    # 'missing_procedures', 'linux', 'windows', 'aix'),('alerts_hard_warning',
    #  'alerts_hard_critical', 'alerts_acknowledged_warning',
    #  'alerts_acknowledged_critical', ))
    list_display = ('date', 'total_host', 'total_services',
        'written_procedures', 'total_written', 'missing_procedures', 'total_missing',
        'linux', 'windows', 'aix', 'comment_host', 'comment_service', 'comment_procedure', 'nb_host_down')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Host & Services', {'fields': ['total_host', 'comment_host', 'total_services', 'comment_service']}),
        ('Operating Systems', {'fields': ['linux', 'windows', 'aix']}),
        ('Procedures', {'fields': ['written_procedures', 'total_written', 'missing_procedures', 'total_missing', 'comment_procedure']}),
    ]

class KpiRedmineAdmin(admin.ModelAdmin):
    """
    modify default settings for kpi redmine
    """
    list_display = ('date', 'requests_opened', 'requests_closed',
        'requests_remained', 'requests_waiting', 'lifetime', 'lifetime_normal', 'lifetime_high',
        'lifetime_urgent', 'comment_lifetime', 'lifetime_aim')
    list_editable = ['requests_waiting']
    date_hierarchy = 'date'
    ordering = ['-date']
    actions = ['update']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Requests', {'fields': ['requests_opened', 'requests_closed', 'requests_remained', 'requests_waiting']}),
        ('Lifetime', {'fields': ['requests_lifetime', 'comment_lifetime', 'requests_lifetime_normal', 'requests_lifetime_high', 'requests_lifetime_urgent', 'aim_lifetime']}),
    ]

    def update(self, request, queryset):
        """
        update database from selected date
        """
        from jobs.insert import insert_redmine

        tzname = timezone.get_current_timezone_name()
        tzinfo = pytz.timezone(tzname)
        for query in queryset:
            date = query.date
        date_locale = tzinfo.normalize(date)
        KpiRedmine.objects.filter(date__gte = date).delete()
        rows_updated = insert_redmine()
        self.message_user(
            request,
            "%s entries successfully updated from %s" % (rows_updated,
                                                    date_locale.strftime("%c")))
        # self.message_user(request, "%s" % (queryset))
    update.short_description = "Update database from selected date"

class NagiosAdmin(admin.ModelAdmin):
    """
    modify default settings for nagios notifications
    """
    list_display = ('date', 'host', 'service', 'app', 'state', 'acknowledged')
    date_hierarchy = 'date'
    ordering = ['-date']
    list_filter = ('acknowledged', 'state', 'app')
    actions = ['update']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'app', 'state', 'acknowledged']}),
    ]
    def update(self, request, queryset):
        """
        update database from last date
        """
        from jobs.insert import insert_nagios_notifications, get_notifications

        tzname = timezone.get_current_timezone_name()
        tzinfo = pytz.timezone(tzname)
        date = NagiosNotifications.objects.order_by('-date')[0].date
        date_locale = tzinfo.normalize(date)
        rows_updated = insert_nagios_notifications(get_notifications())
        self.message_user(
            request,
            "%s new notifications imported from %s" % (rows_updated,
                                                    date_locale.strftime("%c")))
    update.short_description = "Update database"

class CountNotificationsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'warning', 'warning_acknowledged', 'critical',
        'critical_acknowledged','unknown', 'unknown_acknowledged', 'comment_notification_warning', 'comment_notification_warning_ack',
        'comment_notification_critical', 'comment_notification_critical_ack',
        'comment_notification_unknown', 'comment_notification_unknown_ack')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Warning', {'fields': ['warning', 'comment_notification_warning', 'warning_acknowledged', 'comment_notification_warning_ack']}),
        ('Critical', {'fields': ['critical', 'comment_notification_critical', 'critical_acknowledged', 'comment_notification_critical_ack']}),
        ('Unknown', {'fields': ['unknown', 'comment_notification_unknown', 'unknown_acknowledged', 'comment_notification_unknown_ack']}),
    ]

class RecurrentAlertsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'host', 'service', 'frequency')
    ordering = ['-frequency']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'frequency']}),
    ]
    
class RecurrentAlertsWeekAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'host', 'service', 'frequency')
    ordering = ['-frequency']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'frequency']}),
    ]


class OldestAlertsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'host', 'service', 'date_error', 'state', 'acknowledged')
    date_hierarchy = 'date'
    ordering = ['date_error']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'date_error']}),
    ]

class FailedServicesAdmin(admin.ModelAdmin):
    """
    modify default settings for FailedServicesAdmin
    """
    list_display = ('date', 'nb_warning', 'nb_critical', 'nb_unknown', 'nb_acknowledged', 'nb_not_acknowledged', 'nb_host_down', 'nb_oldest_alert')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['nb_warning', 'nb_critical', 'nb_unknown', 'nb_acknowledged', 'nb_not_acknowledged', 'nb_host_down', 'nb_oldest_alert']}),
    ]
    
class CountFailedServicesAdmin(admin.ModelAdmin):
    """
    modify default settings for CountFailedServicesAdmin
    """
    list_display = ('date', 'nb_failed_day', 'nb_failed_week', 'nb_failed_month', 'nb_failed_some_month')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['nb_failed_day', 'nb_failed_week', 'nb_failed_month', 'nb_failed_some_month']}),
    ]
    
class CountFailedServicesByAppsAdmin(admin.ModelAdmin):
    """
    modify default settings for CountFailedServicesByAppsAdmin
    """
    list_display = ('date', 'list_app_graph_data')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['list_app_graph_data']}),
    ]

admin.site.register(KpiNagios, KpiNagiosAdmin)
admin.site.register(KpiRedmine, KpiRedmineAdmin)
admin.site.register(NagiosNotifications, NagiosAdmin)
admin.site.register(CountNotifications, CountNotificationsAdmin)
admin.site.register(RecurrentAlerts, RecurrentAlertsAdmin)
admin.site.register(RecurrentAlertsWeek, RecurrentAlertsWeekAdmin)
admin.site.register(OldestAlerts, OldestAlertsAdmin)
admin.site.register(FailedServices, FailedServicesAdmin)
admin.site.register(CountFailedServices, CountFailedServicesAdmin)
admin.site.register(CountFailedServicesByApps, CountFailedServicesByAppsAdmin)
