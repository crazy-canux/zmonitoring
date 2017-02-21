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
Django views for application nagios.
"""

# Std imports
import logging
import json
import time
from base64 import urlsafe_b64decode

# Django imports
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.shortcuts import render

# Models imports
from apps.nagios.models import Satellite, SecurityPort

# Utilities
from cipher import AESCipher


logger = logging.getLogger(__name__)


# View definitions
# ================
#
def acknowledge_token(request, token):
    """Acknowledge a host or service alert using an encrypted token."""
    time_now = time.time()
    cipher = AESCipher('ABCDEF0123456789', iv='iv1234567890ABCD')
    host_command_line = "COMMAND [{timestamp}] {command};" \
                        "{hostname};" \
                        "{sticky};" \
                        "{notify};" \
                        "{persistent};" \
                        "{author};" \
                        "Ack by email, working on it."
    svc_command_line = "COMMAND [{timestamp}] {command};" \
                       "{hostname};" \
                       "{service_description};" \
                       "{sticky};" \
                       "{notify};" \
                       "{persistent};" \
                       "{author};" \
                       "Ack by email, working on it."

    # Try to decode the encrypted token to a python object (dict)
    try:
        token = str(token)
        json_token = cipher.decrypt(urlsafe_b64decode(token))
        ack_data = json.loads(json_token)
    except:
        logger.exception("Unable to decrypt the provided token !")
        logger.debug("Token received: %s", token)
        return HttpResponse('Token is not valid !\n', status=400)

    # Check token validity in time
    if time_now > ack_data['expire_time']:
        if 'service_description' in ack_data:
            logger.warning(
                "Token validity for service alert \"%s / %s\" has expired !",
                ack_data['hostname'],
                ack_data['service_description'])
        else:
            logger.warning("Token validity for host alert \"%s\" has expired !",
                           ack_data['hostname'])
        return render(request, 'nagios/ack_email_expired.html', ack_data)

    # Send the ack command to Nagios
    if 'service_description' in ack_data:
        command_line = svc_command_line.format(timestamp=time_now,
                                               **ack_data)
    else:
        command_line = host_command_line.format(timestamp=time_now,
                                                **ack_data)

    # Establish a connection to satellites and send the command to ack
    try:
        satellites = Satellite.live_connect()
        for conn in satellites.connections:
            site = conn[0]
            satellites.command(command_line, sitename=site)
    except Satellite.SatelliteConnectError as e:
        logger.exception('Error connecting on satellites !')
        return HttpResponse('Unable to connect to Nagios.\n'
                            'Error: {}\n'.format(e), status=400)

    logger.info("Processed ack by email: %s", command_line)

    return render(request, 'nagios/ack_email_passed.html', ack_data)


def get_satellite_list(request, format='json'):
    """
    Return the list of all satellites, format is json by default.
    """
    satellites = Satellite.objects.filter(active=True)
    if format not in "csv":
        return HttpResponse(serializers.serialize(format, satellites))
    else:
        csv = ""
        for sat in satellites:
            csv += "%s;%s;%s;%s\n" % (sat.name, sat.fqdn, sat.alias, sat.live_port)
        return HttpResponse(csv)


@csrf_exempt
def send_passive(request):
    """
    Web API that uses HTTP POST requests to send passive checks results to Nagios.

    **Note**
        As this is POST data but we have no form, CSRF protection is off for Django using decorator ``@csrf_exempt``.

    You should provides the following POST variables to the URL of the Web API:

    - host
    - service
    - status
    - message

    The view log any received HTTP TRAP to file ``~django/optools/log/http_trap.log`` on Central server. File is rotated.

    How to use with **cURL**
    ------------------------

    This example send a WARNING alert to the service CPU of host NAGIOS_DC_SATELLITE_EDC1::

     curl -f \
     -d host=NAGIOS_DC_SATELLITE_EDC1 \
     -d service=CPU \
     -d status=1 \
     -d message="Test TRAP HTTP" \
     http://canuxcheng.com/optools/nagios/passive/
    """
    # Get the logger for this view
    logger.info('-------------------------------')
    logger.info('-- Receiving a new HTTP TRAP --')
    logger.info('-------------------------------')
    logger.info('From IP: %s', request.META.get('REMOTE_ADDR'))
    logger.info('User-Agent: %s', request.META.get('HTTP_USER_AGENT'))
    logger.debug('Request body: %s', request.body)

    # Livestatus queries
    command_line = 'COMMAND [{timestamp}] PROCESS_SERVICE_CHECK_RESULT;{host};{service};{status};{message}\n'
    query_find_host = 'GET hosts\nColumns: name services\nFilter: name = {host}\n'
    query_find_service = 'GET services\nColumns: description host_name\nFilter: host_name = {host}\nFilter: description = {service}\nAnd: 2\n'

    # Get POST data
    try:
        params = {
            'host': request.POST['host'].upper(),
            'service': request.POST['service'],
            'status': int(request.POST['status']),
            'message': request.POST['message'],
            'timestamp': int(time.time()),
        }
        logger.debug('Cleaned data: %s', params)
    except KeyError:
        logger.exception('Incomplete POST data !')
        return HttpResponse('Incomplete POST data ! Missing key.\n', status=400)
    except ValueError:
        logger.exception('Incorrect value type for data !')
        return HttpResponse('The key \"status\" should be an integer within 0 (OK), 1 (WARNING), 2 (CRITICAL) and 3 (UNKNOWN).\n', status=400)

    # Prepare data to be sent to Nagios
    try:
        satellites = Satellite.live_connect()
        satellites.set_prepend_site(True)
    except Satellite.SatelliteConnectError as e:
        logger.exception('Error connecting on satellites !')
        return HttpResponse('Unable to connect to Nagios.\nError: {}\n'.format(e), status=400)

    # Check if host and service exist in Nagios
    host_dest = satellites.query(query_find_host.format(**params))
    if host_dest:
        # The host is found, check if service exist
        service_dest = satellites.query(query_find_service.format(**params))
        if service_dest:
            sat = service_dest.pop()[0]

            logger.info('Preparing command for Nagios.')
            logger.debug('Command: %s', command_line.format(**params))
            logger.debug('Satellite: %s', sat)

            satellites.command(command_line.format(**params), sitename=sat)
        else:
            # Service not found
            message = 'Service \"{service}\" does not exist on host \"{host}\".\n'.format(**params)
            logger.error(message)
            return HttpResponse(message, status=400)
    else:
        # Host not found
        message = 'The host \"{host}\" does not exist in Nagios.\n'.format(**params)
        logger.error(message)
        return HttpResponse(message, status=400)

    # Everything is OK
    logger.info('HTTP TRAP processed successfully.')
    return HttpResponse()


# Class-based views
class SatelliteListView(ListView):
    """
    Show the list of satellites.
    """
    context_object_name = "systems_list"
    model = Satellite

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SatelliteListView, self).get_context_data(**kwargs)

        # Adding extra context data to the view
        context['section'] = {'systems': 'active'}
        context['base_url'] = self.request.build_absolute_uri('/').strip('/')
        context['ports'] = SecurityPort.objects.all()

        return context
