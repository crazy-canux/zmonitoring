================================================================================
Developper documentation
================================================================================

This is the developper documentation (handbook) for this project. This are
things to know in order to setup your development environment and how works
optools in general.

Your development environment
============================

First we need to configure your environment.

Setup Python virtual env
------------------------

To setup the same virtual environment that the one used in production::

 $ cd optools
 $ mkvirtualenv optools -r ./requirements/production.deps 

Setup local settings
--------------------

Create file ``settings_local.py`` in ``optools`` folder relative to the project
root.

Add the following content in it::

 DEBUG = True
 TEMPLATE_DEBUG = DEBUG
 SECRET_KEY = 'super-top-secret-key'

This snippet enable ``DEBUG`` and development modes. Do not care about security
here this is why the ``SECRET_KEY`` is set to a fake string.

Initialize a test database
--------------------------

Activate the virtual environment::

 $ workon optools

Then, initialize the database used for testing with a default set of data
inside. This will take a while::

 $ ./manage.py syncdb --noinput

You should now have a fully working optools installation. Test it with::

 $ ./manage.py runserver 0:8000

PyCharm
=======

These are PyCharm specific settings. Do not care if not needed.

Team configuration
------------------

The Pycharm's config is shared among us and stored in ``.idea`` folder which is
part of the repository. It includes default run configuration, coding styles,
etc...

Configuring Python interpreter
------------------------------

The Python interpreter should be called ``Python (optools)`` and Python bin set
to ``~/Envs/optools/bin/python``.

Making Changes to a Database Schema
===================================

This is the procedure to apply if you change the database schema for the
project.

- Add the field to your model.

- Run ``manage.py sqlall [yourapp]`` to see the new
CREATE TABLE statement for the model. Note the column definition for the new
field.

- Start your database’s interactive shell (e.g., psql or mysql, or you can
use ``manage.py dbshell``). Execute an ``ALTER TABLE`` statement that adds your
new column.

Cron jobs
=========

Look at the django's user crontab for the list of croned jobs on
monitoring-dc.app.corp::

 $ ssh monitoring-dc.app.corp -l django
 $ crontab -l

Testing Data
============

Here is an example to have some data from production database that you can use
for testing when developing new features.

This example export data about KPI tables (models) from the production database.
This is a JSON export that you can compress and use it on ``monadm.edc.eu.corp``
in your local optools folder.

Logon ``monitoring-dc.app.corp`` as ``django`` user then type::

 $ cd optools
 $ workon optools
 $ python ./manage.py dumpdata kpi > ~/kpi_test_data_20130220.json

Then copy the file ``kpi_test_data_20130220.json`` on the DEV server using scp.
Import data (called fixture in Django) with::

 $ workon optools
 $ python ./manage.py loaddata kpi_test_data_20130220.json

