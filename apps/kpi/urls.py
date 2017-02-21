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

from django.conf.urls import *

urlpatterns = patterns('apps.kpi.indicateurs',
      
    # chart standalone  
    url(r'^reporting/chart_count_failed_services_by_apps/$',
        view='chart_count_failed_services_by_apps_render',
        name='chart_count_failed_services_by_apps'), 
    url(r'^reporting/chart_count_old_alert_vs_host_down/$',
        view='chart_count_old_alert_vs_host_down_render',
        name='chart_count_old_alert_vs_host_down'),
    url(r'^reporting/chart_count_failed_services/$',
        view='chart_count_failed_services_render',
        name='chart_count_failed_services'),
    url(r'^reporting/chart_failed_services/$',
        view='chart_failed_services_render',
        name='chart_failed_services'),
    url(r'^reporting/chart_data_oldests_alerts/$',
        view='chart_data_oldests_alerts_render',
        name='chart_data_oldests_alerts'),
    url(r'^reporting/chart_data_recurrents_alerts_week/$',
        view='chart_data_recurrents_alerts_week_render',
        name='chart_data_recurrents_alerts_week'),
    url(r'^reporting/chart_data_recurrents_alerts/$',
        view='chart_data_recurrents_alerts_render',
        name='reporting_chart_data_recurrents_alerts'),
    url(r'^reporting/chart_data_alerts/$',
        view='chart_data_alerts_render',
        name='reporting_chart_data_alerts'),
    url(r'^reporting/chart_data_nagios/$',
        view='chart_data_nagios_render',
        name='reporting_chart_data_nagios'),
    url(r'^reporting/chart_data_equipement/$',
        view='chart_data_equipement_render',
        name='reporting_chart_data_equipement'),
    url(r'^reporting/chart_redmine/$',
        view='chart_redmine',
        name='reporting_chart_redmine'),

    url(r'^reporting/request_redmine_external/$',
        view='request_redmine_external',
        name='request_redmine_external'),

    url(r'^reporting/$',
        view='indicateurs',
        name='reporting_home'),
)

