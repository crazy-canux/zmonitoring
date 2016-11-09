#!/usr/bin/env python2.7
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

# Std imports
import logging
import sys
import os

# Locate optools settings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Apps imports
from apps.kb.models import Procedure

# Django imports
from django.db import transaction
from django.conf import settings


# Logging
logger = logging.getLogger('jobs.update-kb')

#===============================================================================
#  _____                 _   _
# |  ___|   _ _ __   ___| |_(_) ___  _ __  ___
# | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
#===============================================================================
def init_wiki():
    """Build the index of all KB in dokuwiki (txt files in data/pages folder)."""
    logger.info('Building Procedure index.')
    logger.debug('Pages directory is \"%s\".' % settings.DOKUWIKI_PAGES_DIR)

    index = []

    # Check all procedure files that exist in Dokuwiki
    for root, lsdirs, lsfiles in os.walk(settings.DOKUWIKI_PAGES_DIR):
        lsfiles.sort()
        lsdirs.sort()

        root_namespace = os.path.relpath(root, settings.DOKUWIKI_PAGES_DIR).replace('/', ':')
        if root_namespace != "." and not root_namespace in index:
            index.append(root_namespace)

        for page in lsfiles:
            name = os.path.splitext(page)[0]
            path = os.path.join(root, name)
            namespace = os.path.relpath(path, settings.DOKUWIKI_PAGES_DIR).replace('/', ':')
            if not namespace in index:
                index.append(namespace)

    return index

def push_to_db(index):
    """Push KB to the database, keep in sync with dokuwiki."""
    logger.info("Populating database...")
    with transaction.commit_on_success():
        for kb_name in index:
            procedure, created = Procedure.objects.get_or_create(namespace=kb_name)
            procedure.save()

    logger.info('Done. Database now have %d procedures.', Procedure.objects.count())

def linkify_parents():
    """Make parents relations."""
    logger.info("Linkify parents...")
    with transaction.commit_on_success():
        for procedure in Procedure.objects.all():
            procedure.parents.clear()
            for parent_name in procedure.get_parents():
                parent_model = Procedure.objects.get(namespace=parent_name)
                procedure.parents.add(parent_model)
    logger.info("Done. Parent relations are created.")

def delete_removed(index):
    """Find all KB that no longer exist in dokuwiki and delete them from the database."""
    logger.info("Checking to replicate deletions of KB from wiki to database.")
    kb_in_dokuwiki = set(index)
    kb_in_db = set(Procedure.objects.all())
    deleted_kb = kb_in_db - kb_in_dokuwiki

    for procedure in deleted_kb:
        logger.debug('Kb \"%s\" has been removed from wiki. Deletes database entry.', procedure.namespace)
        procedure.delete()

    logger.info("Done. Deleted %s procedures from database.", len(deleted_kb))

#===============================================================================
#  __  __       _
# |  \/  | __ _(_)_ __
# | |\/| |/ _` | | '_ \
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
#
#===============================================================================

def main():
    """
    Main job procedure.
    """
    logger.info('Starting job: %s.', os.path.basename(__file__))

    kb_index = init_wiki()
    push_to_db(kb_index)
    linkify_parents()
    delete_removed(kb_index)

    logger.info('Ending job: %s.', os.path.basename(__file__))

if __name__ == '__main__':
    main()
