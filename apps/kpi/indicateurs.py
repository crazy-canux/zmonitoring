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

from .models import KpiNagios, KpiRedmine, CountNotifications, RecurrentAlerts, \
    OldestAlerts, RecurrentAlertsWeek, FailedServices, CountFailedServices, \
    CountFailedServicesByApps
from database import redmine
from datetime import datetime, timedelta, date
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.decorators.cache import cache_page
from random import randrange, randint
from sqlalchemy import *
from sqlalchemy.exc import StatementError
import json
import os
import sys





# randomly set html color code
def randomcolor():
    aplha_color = {
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F'
    }

    alea_color = '#'
    i = 0
    while i < 6:
        lettre = aplha_color[randint(10, 15)]
        n = randrange(0, 15, 2)
        if n > 9:
            val = aplha_color[n]
        else:
            val = str(n)
        alea_color += val + lettre
        i += 2

    return alea_color


def request_redmine_external(request):
    # Establish Redmine database connection
    redmine_db_connection = redmine.engine.connect()
    requete = redmine.issues.join(
        redmine.Projects,
        redmine.IssueStatus,
        redmine.CustomValues).filter(
            redmine.IssueStatus.is_closed == False,
            redmine.CustomValues.value=='External').order_by(
                redmine.Issues.created_on.desc())
    char_temp_json = "jsoncallback(["
    try:
        for data in requete:
            char_temp_json += "{"
            char_temp_json += "'id':'%s'"  % (data.id)
            char_temp_json += ",'created_on':'%s'"  % ( str(data.created_on))

            if data.user_assigned:
                user_assigned = data.user_assigned.lastname.decode('cp1252').encode('utf-8') + " " + data.user_assigned.firstname.decode('cp1252').encode('utf-8')
            else:
                user_assigned = ""

            if data.user_created:
                user_created = data.user_created.lastname.decode('cp1252').encode('utf-8') + " " + data.user_created.firstname.decode('cp1252').encode('utf-8')
            else:
                user_created = ""

            char_temp_json += ",'user_assigned':'%s'"  % (user_assigned.replace("'", '"'))

            char_temp_json += ",'user_created':'%s'" % (user_created.replace("'", '"'))

            char_temp_json += ",'project_name':'%s'"  % (data.project.name.replace("'", '"'))

            char_temp_json += ",'subject':'%s'"  % (data.subject.replace("'", '"'))

            char_temp_json += ",'status_name':'%s'" % (data.status.name.replace("'", '"'))

            char_temp_json += ",'priority_id':'%s'" % (data.priority_id)

            char_temp_json += "}"

            char_temp_json += ",\n"
    finally:
        redmine_db_connection.close()

    char_temp_json = char_temp_json[:-2]
    char_temp_json += "])"

    return HttpResponse(char_temp_json, content_type="application/json")


def chart_red():
    today_date = date.today()
    last_year_date = today_date - timedelta(days=365)

    kpi_redmine = KpiRedmine.objects.filter(
        date__range=(last_year_date, today_date))

    chart = "[\n"

    for index, kpi in enumerate(kpi_redmine):
        lifetime = kpi.requests_lifetime / 3600
        lifetime_external = kpi.requests_lifetime_low_external / 3600
        lifetime_normal = kpi.requests_lifetime_normal / 3600
        lifetime_high = kpi.requests_lifetime_high / 3600
        lifetime_urgent = kpi.requests_lifetime_urgent / 3600
        lifetime_aim = kpi.aim_lifetime / 3600
        url = "http://canuxcheng.com/tracking/activity?from="
        url += '%d-%d-%d' % (kpi.date.year, kpi.date.month, kpi.date.day)

        chart += '{date: new Date("%s"), remained: %d,remained_external: %d, '\
            'opened: %d, closed: %d, opened_external: %d, closed_external: %d, global: %d, '\
            'lifetime_external : %d, normal: %d, high: %d, urgent: %d, url: "%s", '\
            'comment_lifetime: "%s", lifetime_aim: %d' % (
                kpi.date.isoformat(),
                kpi.requests_remained,
                kpi.requests_remained_external,
                kpi.requests_opened,
                kpi.requests_closed,
                kpi.requests_opened_external,
                kpi.requests_closed_external,
                lifetime,
                lifetime_external,
                lifetime_normal,
                lifetime_high,
                lifetime_urgent,
                url,
                kpi.comment_lifetime.replace("\r\n", "\\n").replace('"',"'"),
                lifetime_aim)

        if kpi.requests_waiting is not None:
            chart += ', requests_waiting: %d' % kpi.requests_waiting
        if kpi.requests_waiting is not None:
            chart += ', requests_waiting_external: %d' % kpi.requests_waiting_external
        chart += '}'

        if index != len(kpi_redmine)-1:
            chart += ",\n"

    chart += "\n]"

    return chart

@cache_page(14400)
def chart_redmine(request):

    chart = chart_red()

    local_context = {
        "name_chart": "chartDataRequest",
        "chart": chart,
        "function_launched": 'createRequests("tv_view");',
        "graph": "graphRequest",
        "title_graph": "Requests <small>additions &amp; changes</small>",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_data_nagios():
    today_date = date.today()
    last_year_date = today_date - timedelta(days=365)
    chart = "[\n"
    kpi_nagios = KpiNagios.objects.filter(
        date__range=(last_year_date, today_date))

    for index, kpi in enumerate(kpi_nagios):
        chart += '{date: new Date("%s"), total_host: %d, '\
        'total_services: %d, total_app: %d,'\
        'linux: %d, windows: %d, aix: %d, comment_host: "%s", comment_service: "%s", nb_host_down : %d}' % (
            kpi.date.isoformat(),
            kpi.total_host,
            kpi.total_services,
            kpi.total_app,
            kpi.linux,
            kpi.windows,
            kpi.aix,
            kpi.comment_host.replace("\r\n", "\\n"),
            kpi.comment_service.replace("\r\n", "\\n"),
            kpi.nb_host_down)

        if index != len(kpi_nagios)-1:
            chart += ",\n"

    chart += "\n]"
    return chart

@cache_page(14400)
def chart_data_equipement_render(request):

    chart = chart_data_nagios()

    local_context = {
        "name_chart": "chartDataNagios",
        "chart": chart,
        "function_launched": 'createEquipements("tv_view");',
        "graph": "graphEquipement",
        "title_graph": "Operating System Repartition <small>as seen in Nagios</small>",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

@cache_page(14400)
def chart_data_nagios_render(request):

    chart = chart_data_nagios()

    local_context = {
        "name_chart": "chartDataNagios",
        "chart": chart,
        "function_launched": 'createHosts("tv_view");',
        "graph": "graphHosts",
        "title_graph": "Hosts & Services <small>monitored in Nagios</small>",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_data_alerts():
    today_date = date.today()
    last_year_date = today_date - timedelta(days=365)

    result = CountNotifications.objects.filter(
        date__range=(last_year_date, today_date))

    chart_data_alerts = "[\n"

    for alert in result:
        chart_data_alerts += '{date: new Date("%s"), warning: %d, '\
            ' critical: %d, '\
            ' unknown: %d,'\
            ' total_alerts_ack: %d,'\
            ' total_alerts: %d }' % (
            alert.date.isoformat(),
            alert.warning ,
            alert.critical ,
            alert.unknown ,
            (alert.warning_acknowledged + alert.critical_acknowledged + alert.unknown_acknowledged),
            (alert.warning + alert.critical + alert.unknown ))

        chart_data_alerts += ",\n"

    chart_data_alerts += "\n]"

    return chart_data_alerts

@cache_page(14400)
def chart_data_alerts_render(request):

    chart_data_alerts_graph = chart_data_alerts()
    local_context = {
        "name_chart": "chartDataAlerts",
        "chart": chart_data_alerts_graph,
        "function_launched": 'createAlerts("tv_view");',
        "graph": "graphAlerts",
        "title_graph": "Alerts <small>triggered by Nagios to Omnibus</small>",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_data_recurrents_alerts():
    chart_data_recurrents_alerts = "[\n"

    others = RecurrentAlerts.objects.all()
    recurrents_alerts = others.order_by("-frequency")[:15]
    number_others = 0

    for alert in recurrents_alerts:
        serv = alert.service
        if serv:
            serv += "@"
        chart_data_recurrents_alerts += '{name: "%s%s", repetitions: %d, date_last_alert: "%s", '\
        'url: "http://canuxcheng.com/thruk/cgi-bin/status.cgi?host=%s"}' % (
            serv,
            alert.host,
            alert.frequency,
            alert.date,
            alert.host)
        chart_data_recurrents_alerts += ",\n"
    for alert in others:
        number_others += alert.frequency

    chart_data_recurrents_alerts += "\n]"

    return chart_data_recurrents_alerts, number_others


@cache_page(14400)
def chart_data_recurrents_alerts_render(request):

    temp = chart_data_recurrents_alerts()
    chart_data_recurrents_alerts_graph = temp[0]
    number_others = temp[1]

    local_context = {
        "name_chart": "chartDataRecurrentsAlerts",
        "chart": chart_data_recurrents_alerts_graph,
        "function_launched": 'createRecurrentsAlerts("tv_view");',
        "graph": "graphRecurrentsAlerts",
        "title_graph": "Recurrents Alerts <span style='font-size: 15px;'>(only hard state per services with notifications enabled and not in downtime)</span> ",
        "other": number_others,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_data_recurrents_alerts_week():
    chart_data_recurrents_alerts_week = "[\n"

    others = RecurrentAlertsWeek.objects.all()
    recurrents_alerts = others.order_by(
        "-frequency")[:15]
    number_others_weeks = 0

    for alert in recurrents_alerts:
        serv = alert.service
        if serv:
            serv += "@"
        chart_data_recurrents_alerts_week += '{name: "%s%s", repetitions: %d, date_last_alert:"%s", '\
        'url: "http://canuxcheng.com/thruk/cgi-bin/status.cgi?host=%s"}' % (
            serv,
            alert.host,
            alert.frequency,
            alert.date,
            alert.host)
        chart_data_recurrents_alerts_week += ",\n"
    for alert in others:
        number_others_weeks += alert.frequency
    chart_data_recurrents_alerts_week += "\n]"

    return chart_data_recurrents_alerts_week, number_others_weeks

@cache_page(14400)
def chart_data_recurrents_alerts_week_render(request):

    temp_week = chart_data_recurrents_alerts_week()
    chart_data_recurrents_alerts_week_graph = temp_week[0]
    number_others_weeks = temp_week[1]

    local_context = {
        "name_chart": "chartDataRecurrentsAlertsWeek",
        "chart": chart_data_recurrents_alerts_week_graph,
        "function_launched": 'createRecurrentsAlertsWeek("tv_view");',
        "graph": "graphRecurrentsAlertsWeek",
        "title_graph": "Recurrents Alerts Week <span style='font-size: 15px;'>(only hard state per services with notifications enabled and not in downtime)</span> ",
        "other": number_others_weeks,
        "other_name":"others_weeks"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_data_oldests_alerts():

    color_list = []

    chart_data_oldests_alerts = "[\n"
    oldest_alerts = OldestAlerts.objects.all().order_by("date_error")[:20]
    for alert in oldest_alerts:
        days = alert.date - alert.date_error
        date_error = "%s-%s-%s" % (
            alert.date_error.year,
            alert.date_error.month,
            alert.date_error.day)
        days = days.total_seconds()/60/60/24
        serv = alert.service

        color_graph = randomcolor()
        while color_graph in color_list:
            color_graph = randomcolor()

        color_list.append(color_graph)

        if serv:
            serv += "@"
        chart_data_oldests_alerts += \
            '{name: "%s%s", days: %d, date_error: "%s", ' \
            'url: \"http://canuxcheng.com/thruk/cgi-bin/status.cgi?host=%s" , ' \
            'color_graph: "%s"}' % (
                serv,
                alert.host,
                days,
                date_error,
                alert.host,
                color_graph
            )
        chart_data_oldests_alerts += ",\n"

    chart_data_oldests_alerts += "\n]"

    return chart_data_oldests_alerts

@cache_page(14400)
def chart_data_oldests_alerts_render(request):

    chart_data_oldests_alerts_graph = chart_data_oldests_alerts()
    local_context = {
        "name_chart": "chartDataOldestsAlerts",
        "chart": chart_data_oldests_alerts_graph,
        "function_launched": 'createOldestsAlerts("tv_view");',
        "graph": "graphOldestsAlerts",
        "title_graph": "Oldests Alerts <span style='font-size: 15px;'>active in Nagios (with notifications enabled and not in downtime)</span>",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_failed_services():

    chart_failed_services = "[\n"
    kpi_failed_services = FailedServices.objects.all().order_by("date")

    for index, kpi in enumerate(kpi_failed_services):
        chart_failed_services += '{date: new Date("%s"), nb_warning: %d, '\
        'nb_critical: %d, nb_unknown: %d,'\
        'nb_acknowledged: %d, nb_not_acknowledged: %d, nb_host_down: %d}' % (
            kpi.date.isoformat(),
            kpi.nb_warning,
            kpi.nb_critical,
            kpi.nb_unknown,
            kpi.nb_acknowledged,
            kpi.nb_not_acknowledged,
            kpi.nb_host_down)

        if index != len(kpi_failed_services)-1:
            chart_failed_services += ",\n"

    chart_failed_services += "\n]"
    return chart_failed_services

@cache_page(14400)
def chart_failed_services_render(request):

    chart_failed_services_graph = chart_failed_services()
    local_context = {
        "name_chart": "chartFailedServices",
        "chart": chart_failed_services_graph,
        "function_launched": 'createFailedServices("tv_view");',
        "graph": "graphFailed",
        "title_graph": "Failed Services repartition per status",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_count_failed_services():
    chart_count_failed_services = "[\n"
    kpi_count_failed_services = CountFailedServices.objects.all().order_by("date")

    for index, kpi in enumerate(kpi_count_failed_services):
        chart_count_failed_services += '{date: new Date("%s"), nb_failed_day: %d, '\
        'nb_failed_week: %d, nb_failed_month: %d,'\
        'nb_failed_some_month: %d}' % (
            kpi.date.isoformat(),
            kpi.nb_failed_day,
            kpi.nb_failed_week,
            kpi.nb_failed_month,
            kpi.nb_failed_some_month)

        if index != len(kpi_count_failed_services)-1:
            chart_count_failed_services += ",\n"

    chart_count_failed_services += "\n]"

    return chart_count_failed_services

@cache_page(14400)
def chart_count_failed_services_render(request):

    chart_count_failed_services_graph = chart_count_failed_services()

    local_context = {
        "name_chart": "chartCountFailedServices",
        "chart": chart_count_failed_services_graph,
        "function_launched": 'createCountFailedServices("tv_view");',
        "graph": "graphCountFailed",
        "title_graph": "Failed Services repartition per duration",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_count_old_alert_vs_host_down():
    chart_count_old_alert_vs_host_down = "[\n"

    kpi_failed_services = FailedServices.objects.all().order_by("date")

    for index, kpi in enumerate(kpi_failed_services):
        chart_count_old_alert_vs_host_down += '{date: new Date("%s"), nb_host_down: %d, '\
        'nb_oldest_alert: %d}' % (
            kpi.date.isoformat(),
            kpi.nb_host_down,
            kpi.nb_oldest_alert)

        if index != len(kpi_failed_services)-1:
            chart_count_old_alert_vs_host_down += ",\n"

    chart_count_old_alert_vs_host_down += "\n]"

    return chart_count_old_alert_vs_host_down

@cache_page(14400)
def chart_count_old_alert_vs_host_down_render(request):

    chart_count_old_alert_vs_host_down_graph = chart_count_old_alert_vs_host_down()

    local_context = {
        "name_chart": "chartCountOldAlertVsHostDown",
        "chart": chart_count_old_alert_vs_host_down_graph,
        "function_launched": 'createOldAlertVsHostDown("tv_view");',
        "graph": "graphOldAlertVsHostDown",
        "title_graph": "Oldest Alerts vs Hosts Down",
        "other": 0,
        "other_name":"other"

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)

def chart_count_failed_services_by_apps():
    # filter app
    full_list = {}

    request_graph_failed_by_app = CountFailedServicesByApps.objects.all().values('list_app_graph_data').order_by("-date")
    for data in request_graph_failed_by_app:
        for data_second in json.loads(str(data['list_app_graph_data'])):
            if not str(data_second['app']) in full_list:
                full_list[str(data_second['app'])] = []
            full_list[str(data_second['app'])].append(data_second)

    sort_app = []
    for key,data in full_list.iteritems():
        if not isinstance(data[0]['app'],type(None)):
            sort_app.append([data[0]['nb_app'], data[0]['app']])
    sort_app.sort()
    sort_app.reverse()


    data_set=""
    chart_alert_by_app = ""
    for key_tab, name_app in sort_app:

        data_set += "var dataSet"+str(name_app).replace("-","_").replace(" ","_")+" = new AmCharts.DataSet();\n\
    dataSet"+str(name_app).replace("-","_").replace(" ","_")+".title = \""+str(name_app)+"\";\n\
    dataSet"+str(name_app).replace("-","_").replace(" ","_")+".fieldMappings = [{\
        fromField: \"nb_app\",\
        toField: \"value\"\
    }];"
        chart_alert_by_app = "[\n"
        full_list[name_app].reverse()
        for data in full_list[name_app]:

            chart_alert_by_app += '{date: new Date("%s"), app: "%s", '\
            'nb_app: %d}' % (
                data['date'],
                data['app'],
                data['nb_app'])

            chart_alert_by_app += ",\n"
        chart_alert_by_app = chart_alert_by_app[:-2]
        chart_alert_by_app += "\n]"
        data_set += "dataSet"+str(name_app).replace("-","_").replace(" ","_")+".dataProvider = "+chart_alert_by_app+";\n\
            dataSet"+str(name_app).replace("-","_").replace(" ","_")+".categoryField = \"date\";\n\
        chart.dataSets.push(dataSet"+str(name_app).replace("-","_").replace(" ","_")+"); \n"
    return data_set

@cache_page(14400)
def chart_count_failed_services_by_apps_render(request):

    data_set = chart_count_failed_services_by_apps()
    local_context = {
        "name_chart": "chartC",
        "chart": 0,
        "function_launched": 'createFailedAlertByApp("tv_view");',
        "graph": "chartApp",
        "title_graph": "Number of alerts per application",
        "other": 0,
        "other_name":"other",
        "data_set": data_set

    }
    return render(request, 'kpi/graph_alone/tv_base.html', local_context)


# Cache the page during 24 hours
def indicateurs(request):
    """
    View showing the charts for the differents kpi requested
    param: http request
    """
    section = dict({'kpi': "active"})
    title = "Reporting"

    today_date = date.today()
    last_year_date = today_date - timedelta(days=365)

    # generate redmine data graph
    chart_data_request = chart_red()

    # generate data nagios graph
    chart_data_nagios_graph = chart_data_nagios()

    # generate data alert graph
    chart_data_alerts_graph = chart_data_alerts()

    # generate data recurent
    temp = chart_data_recurrents_alerts()
    chart_data_recurrents_alerts_graph = temp[0]
    number_others = temp[1]

    #generate data recurrent week
    temp_week = chart_data_recurrents_alerts_week()
    chart_data_recurrents_alerts_week_graph = temp_week[0]
    number_others_weeks = temp_week[1]

    chart_data_oldests_alerts_graph = chart_data_oldests_alerts()

    chart_failed_services_graph = chart_failed_services()

    chart_count_failed_services_graph = chart_count_failed_services()

    chart_count_old_alert_vs_host_down_graph = chart_count_old_alert_vs_host_down()

    data_set = chart_count_failed_services_by_apps()

    # Choose template to render
    if request.GET.get('action') == 'print':
        tpl = 'kpi/kpi_print_page.html'
    else:
        tpl = 'kpi/kpi_one_page.html'

    local_context = {
        "today": today_date,
        "chart_data_recurrents_alerts": chart_data_recurrents_alerts_graph,
        "chart_data_recurrents_alerts_week": chart_data_recurrents_alerts_week_graph,
        "chart_data_alerts": chart_data_alerts_graph,
        "chart_data_request": chart_data_request,
        "chart_data_nagios": chart_data_nagios_graph,
        "chart_failed_services": chart_failed_services_graph,
        "chart_count_failed_services": chart_count_failed_services_graph,
        "chart_count_old_alert_vs_host_down": chart_count_old_alert_vs_host_down_graph,
        "number_others": number_others,
        "number_others_weeks": number_others_weeks,
        "chart_data_oldests_alerts": chart_data_oldests_alerts_graph,
        "data_set": data_set,
    }
    return render(request, tpl, local_context)
