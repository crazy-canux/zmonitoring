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

# Std imports
import logging

# Django imports
from django.db import models
from django.core.exceptions import ValidationError

# Apps imports
import apps.nagios.livestatus as live


# Logger for this app
logger = logging.getLogger(__name__)


# Validators
def validate_network_high_port(value):
    if not 1024 < value < 65536:
        raise ValidationError(u'Port number should be between 1024 - 65535')


def validate_network_port(value):
    if not 0 < value < 65536:
        raise ValidationError(u'Port number should be between 1 - 65535')


# Models
class Satellite(models.Model):
    """Model representing list of active Nagios satellites"""
    name = models.CharField(max_length=255, verbose_name='Satellite name',
                            help_text='Example for Hagenbach: HGB')
    active = models.BooleanField(
        default=False,
        verbose_name='Satellite is active',
        help_text='Is this satellite active for production ?')
    is_gearman = models.BooleanField(
        default=False,
        verbose_name='This is a Nagios/Gearman Satellite',
        help_text='Is this a Nagios/Gearman Satellite ?')

    # Network settings
    alias = models.CharField(
        max_length=255,
        verbose_name='Satellite alias',
        help_text='Please use following format: nagios.sss.cc.corp')
    fqdn = models.CharField(
        max_length=255,
        verbose_name='Satellite long name',
        help_text='Fully qualified domain name for the satellite')

    # Livestatus
    ip_address = models.IPAddressField()
    live_port = models.PositiveIntegerField(
        default=6557,
        validators=[validate_network_high_port],
        verbose_name='Livestatus port',
        help_text='Port must be between 1024 - 65536'
    )
    nagios_url = models.CharField(
        max_length=10,
        default='/nagios',
        verbose_name='Base URL',
        help_text='Use at your own risk ! Let it be default if you don\'t '
                  'know what you are doing')

    class Meta:
        ordering = ['name']

    # Exceptions classes for Livestatus connectivity
    class SatelliteConnectError(Exception):
        """
        Exception raised when a satellite is dead.
        """
        def __init__(self, *args, **kwargs):
            super(Satellite.SatelliteConnectError, self).__init__(*args,
                                                                  **kwargs)
            self.dead_satellites = args[0]

        def __str__(self):
            message = "Unable to connect / query satellites: "
            sat_errors = []
            for sat, value in self.dead_satellites.iteritems():
                sat_errors.append('{} ({})'.format(sat, value['exception']))
            message += ', '.join(sat_errors)

            return message

    # Customize livestatus connection class
    class SatelliteConnection(live.MultiSiteConnection):
        """
        Query / Connect to Livestatus peers.
        """
        def query(self, query, add_headers=""):
            q = live.MultiSiteConnection.query(self, query, add_headers)
            if self.dead_sites():
                exc = Satellite.SatelliteConnectError(self.dead_sites())
                logger.exception(exc)
                logger.info("Executed query:\n%s", query)
                raise exc

            return q

    # Livestatus related methods
    def as_live_dict(self, timeout=30):
        """
        Return a dict as expected for :meth:`live.MultiSiteConnection` method.
        """
        return {self.name: {
            'alias': self.alias,
            'socket': 'tcp:{0}:{1}'.format(self.ip_address, self.live_port),
            'nagios_url': self.nagios_url,
            'timeout': timeout,
            }}

    @staticmethod
    def live_connect(retries=3, *args, **kwargs):
        """
        Establish a connection to all satellites using livestatus.
        Returns the livestatus connection MultiSiteConnection object.

        :param timeout: the number of secs before connection is timed out.
        Default to 5 secs.
        :param retries: the number of retries if a satellite has failed.
        """
        satellites = Satellite.objects.filter(active=True)
        connection = None
        connection_settings = {}

        for sat in satellites:
            connection_settings.update(sat.as_live_dict(*args, **kwargs))

        for retry in xrange(0, retries):
            connection = Satellite.SatelliteConnection(connection_settings)
            if not connection.dead_sites():
                break

        if connection.dead_sites():
            exc = Satellite.SatelliteConnectError(connection.dead_sites())
            logger.exception(exc)
            raise exc

        return connection

    # String representation
    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.alias)


class SecurityPort(models.Model):
    """
    Store port information needed on Firewalls in order to allow access from
    Nagios to monitored hosts.
    """
    NETWORK_PROTOCOL = (
        ('ICMP', 'ICMP'),
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
        ('TCP/UDP', 'TCP/UDP'),
    )

    name = models.CharField(max_length=64, help_text='Port name. eg. SNMP, SSH, etc...')
    description = models.CharField(max_length=128, help_text='Enter a description for this port.')
    begin_port = models.PositiveIntegerField(max_length=5, validators=[validate_network_port], help_text='Enter the begin port number.')
    end_port = models.PositiveIntegerField(max_length=5, validators=[validate_network_port], help_text='Enter the end port number. Keep it empty if none.', null=True, blank=True)
    protocol = models.CharField(max_length=7, choices=NETWORK_PROTOCOL, help_text='Choose the network protocol to use.')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
