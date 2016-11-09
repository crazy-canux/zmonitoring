"""
Django views for application kb.
"""

# Std imports
import logging
from pprint import pformat

# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Models imports
from apps.kb.models import Procedure


logger = logging.getLogger(__name__)

@login_required
def show_kb(request, kb_namespace):
    """
    Handle the way KB is shown.

    Try to find the first procedure found in ``kb_namespace``. Redirect to first found if
    the requested procedure is not found and user is not a KB Manager.

    For peoples member of group **kb_manager**, propose to create the procedure
    if missing (all namespaces).

    For others, it says that the procedure is missing and the alert should be
    part of a Stratos ticket to the relevant group.

    :param kb_namespace: the dokuwiki procedure page of the form ``xxx:xxx:xxx...``.

    Template:
        kb/manage_procedure.html

    Context:
        title
        show_main_menu
        kb_found
        kb_requested
        user_is_helpdesk
        procedure_pages
    """
    try:
        logger.info('User \'%s\' (%s) is requesting the KB: \'%s\'',
            request.user.username, ",".join(request.user.groups.values_list('name', flat=True)), kb_namespace)
    except:
        logger.info('Guest user is requesting the KB: \'%s\'', kb_namespace)

    user_is_helpdesk = request.user.groups.filter(name='helpdesk').exists()
    procedure_pages = []
    kb_found = None

    # Init the KB object...
    try:
        kb_requested = Procedure.objects.get(namespace=kb_namespace)
    except Procedure.DoesNotExist:
        kb_requested = Procedure.register(namespace=kb_namespace)

    # .. and its parents
    for parent in kb_requested.get_parents():
        try:
            parent_model = Procedure.objects.get(namespace=parent)
        except Procedure.DoesNotExist:
            parent_model = Procedure.register(namespace=parent)

        procedure_pages.append(parent_model)
    procedure_pages.append(kb_requested)

    # Try to find if there is any procedure existing in the namespace
    for page in procedure_pages:
        if page.is_written:
            kb_found = page

    # Populate the context
    context = {
        'title': "Showing KB %s" % kb_requested.namespace,
        'show_main_menu': False,
        'kb_found': kb_found,
        'kb_requested': kb_requested,
        'user_is_helpdesk': user_is_helpdesk,
        'procedure_pages': procedure_pages,
    }

    logger.debug('Debugging context for rendering template for KB...\n%s', pformat(context))

    # Redirect to the procedure if the requested is created
    if kb_requested and kb_requested.is_written:
        return redirect(kb_requested.get_read_url())
    # Redirect to the first procedure found if user is not helpdesk
    if kb_found and (user_is_helpdesk or request.user.is_anonymous()):
        return redirect(kb_found.get_read_url())
    # No procedure exist or user is not helpdesk
    else:
        return render(request, "kb/manage_procedure.html", context)
