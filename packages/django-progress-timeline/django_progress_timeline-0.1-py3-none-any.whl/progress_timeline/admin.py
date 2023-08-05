# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import CurrentProgress, ProgressTimeLine



class CurrentProgressInline(admin.TabularInline):
    model = CurrentProgress
    classes = ['collapse']
    extra = 0


class ProgressTimeLineAdmin(admin.ModelAdmin):
    model = ProgressTimeLine
    inlines = [CurrentProgressInline, ]
    readonly_fields = ('preview', 'get_number_label')
    fieldsets = (
        (_('basic data'), {
            'fields': (('get_number_label',), ('title', 'goal', 'number_layout'), 'description'),
        }),
        (_('date'), {
            'fields': (('start_date', 'end_date', 'date_layout'),),
        }),
        (_('colors'), {
            'fields': (('background_color', 'basic_color', 'diff_color', 'progress_color'),),
        }),
        (_('preview'), {
            'fields': (('preview', ),),
        }),
    )

    class Media:
        js = ("js/progress_timeline/js.js", )

admin.site.register(CurrentProgress)
admin.site.register(ProgressTimeLine, ProgressTimeLineAdmin)
