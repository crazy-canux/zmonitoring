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

from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

handler500 = 'monitoring.webui.views.server_error'

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Applications
    # ============
    #
    # Portal
    (r'', include('apps.portal.urls')),
    (r'', include('monitoring.webui.urls')),
    (r'', include('apps.kpi.urls')),
    (r'^nagios/', include('apps.nagios.urls')),
    (r'^kb/', include('apps.kb.urls')),
)

