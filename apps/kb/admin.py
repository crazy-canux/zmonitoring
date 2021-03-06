# Adding models to Admin site for kb app

import csv

# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin
from django.utils.encoding import smart_str

# Models imports
from apps.kb.models import Procedure

# Forms imports
from apps.kb.forms import ProcedureCommentForm


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'wiki', 'rating', 'comment', 'validated', 'is_written', 'author', 'last_modified')
    list_filter = ('rating', 'validated', 'is_written')
    search_fields = ['^namespace']
    list_per_page = 15
    ordering = ['-last_modified', 'is_written']

    actions = ['export_csv', 'rate_and_comment', 'unvalidate']

    # Extra fields
    def wiki(self, instance):
        """Show a link to read the procedure online."""
        return '<a href=\"javascript:void(0);\" ' \
               'onclick=\"window.open(\'{}\',\'{}\', ' \
               '\'width=980,height=700\');\">' \
               'Read</a>'.format(instance.get_read_url(), instance)
    wiki.allow_tags = True

    # Disable delete_selected action
    def get_actions(self, request):
        actions = super(ProcedureAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Export to CSV Action
    def export_csv(self, request, queryset):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=wi_list.csv'
        writer = csv.writer(response, csv.excel)
        writer.writerow([
            smart_str(u"Namespace"),
            smart_str(u"Is written ?"),
            smart_str(u"Author"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.namespace),
                smart_str(obj.is_written),
                smart_str(obj.author),
            ])
        return response
    export_csv.short_description = u"Export CSV"

    # Rating Actions
    def rate_and_comment(self, request, queryset):
        comment_form = None
        ids = []

        if 'comment' in request.POST:
            comment_form = ProcedureCommentForm(request.POST)
            if comment_form.is_valid():
                num = queryset.count()
                comment = comment_form.cleaned_data['comment']
                rating = comment_form.cleaned_data['rating']
                rating_key = dict(comment_form.fields['rating'].choices)[int(rating)]

                queryset.update(comment=comment, rating=rating, validated=True)
                for obj in queryset:
                    self.log_change(request, obj, "Changed rating to \"%s\"." % obj.get_rating_display())

                if num == 1:
                    message_bit = "1 procedure was"
                else:
                    message_bit = "%s procedures were" % num
                self.message_user(request, '%s rated as %s.' % (message_bit, rating_key))

                return HttpResponseRedirect(request.get_full_path())

        if '_selected_action' in request.POST:
            ids = request.POST.getlist('_selected_action')

        if not comment_form:
            comment_form = ProcedureCommentForm()

        context = {
            'title': 'Rate selected procedures',
            'section': {'kb': 'active'},
            'procedures': queryset,
            'comment_form': comment_form,
            'ids': ids,
        }

        return render(request, "kb/rate.html", context)
    rate_and_comment.short_description = 'Rate selected procedures'

    def unvalidate(self, request, queryset):
        """Admin action to unvalidate selected procedures."""
        num = queryset.count()
        queryset.update(validated=False)

        if num == 1:
            message_bit = "1 procedure was"
        else:
            message_bit = "%s procedures were" % num
        self.message_user(request, '%s unvalidated successfully.' % message_bit)
    unvalidate.short_description = 'Unvalidate selected procedures'

# Register in admin site
admin.site.register(Procedure, ProcedureAdmin)
