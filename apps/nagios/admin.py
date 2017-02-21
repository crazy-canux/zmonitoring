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

# Adding models to Admin site for Nagios app

from django.contrib import admin
from apps.nagios.models import Satellite, SecurityPort

class SatelliteAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'active', 'is_gearman', 'alias', 'fqdn', 'ip_address')
    list_filter = ('active',)
    fieldsets = (
        (None, {
            'fields': ('name', 'active', 'is_gearman')
        }),
        ('Network settings', {
            'fields': ('ip_address', 'alias', 'fqdn')
        }),
        ('Livestatus settings', {
            'classes': ('collapse',),
            'fields': ('live_port', 'nagios_url')
        }),
    )


class SecurityPortAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'protocol', 'begin_port', 'end_port')
    fieldsets = (
        ('Indentity', {
            'fields': ('name', 'description', 'protocol')
        }),
        ('Range', {
            'fields': ('begin_port', 'end_port')
        }),
    )


admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(SecurityPort, SecurityPortAdmin)

