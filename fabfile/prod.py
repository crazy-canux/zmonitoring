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

from fabric.api import (
    env, task, hosts, cd, prefix, settings, puts, run, sudo, execute)
from fabric.colors import green, cyan


PROD_DEPS = "requirements/production.deps"


def apache_reload():
    """
    Reload Apache service to restart the WSGI process.
    """
    puts(green('Reloading Apache server...'))
    sudo('service apache2 force-reload', shell=False)


@task
@hosts('monitoring-dc.app.corp')
def update(collectstatic=True):
    """Apply latest updates on project in production."""
    from fabfile import util

    env.user = 'django'

    puts(green('Updating project\'s...', bold=True))

    puts(cyan('- Applying update...'))
    with cd('optools'):
        run('git fetch -p')
        run('git reset --hard origin/master')

    # Collect static files
    if collectstatic:
        util.collectstatic()

    # Clean Django cache
    execute(util.cacheclean)

    # Reload Apache
    apache_reload()


@task
@hosts('monitoring-dc.app.corp')
def install():
    """Install the project in production."""
    from fabfile import util

    env.user = 'django'

    # Clone / update the repository
    with settings(warn_only=True):
        if run('test -d optools').failed:
            with cd('$HOME'):
                puts(green('Clone git repository...'))
                run('git clone /git/repositories/admin/optools.git')
                run('mkdir -p /var/www/static/optools')
                run('mkdir -p ~/public_html/reporting')
        else:
            update(collectstatic=False)

    # Create the virtualenv for the project
    puts(green('Creating Python virtual environment...'))
    with cd('optools'):
        run('mkvirtualenv optools -r %s' % PROD_DEPS)

    puts(green('Updating Python virtual environment...'))
    with prefix('workon optools'), cd('optools'):
        run('pip install -U --no-deps -r %s' % PROD_DEPS)
        run('pip install -r %s' % PROD_DEPS)

    # Setup Apache config
    with cd('~django/optools'), settings(user='root'):
        puts(green('Install Apache\'s configuration...'))
        run('ln -sf '
            '~django/optools/apache/django_optools '
            '/etc/apache2/conf.d/django_optools')
        run('service apache2 force-reload')

    # Collect static files
    util.collectstatic()

    # Reload Apache
    apache_reload()
