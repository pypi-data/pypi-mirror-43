# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .fields import ColorField


class ProgressTimeLine(models.Model):

    SHOW_ALL = 0
    ONLY_EDGE = 1
    EMPTY = 2

    DATE_LAYOUT = (
        (SHOW_ALL, _('show all')),
        (ONLY_EDGE, _('only start and end date')),
        (EMPTY, _('do not display'))
    )

    PERCENT = 0
    NUMBERS = 1
    NUMBER_LAYOUT = (
        (PERCENT, _('percent')),
        (NUMBERS, _('numbers')),
        (EMPTY, _('do not display'))
    )

    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    goal = models.IntegerField(verbose_name=_('goal'))

    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))

    date_layout = models.PositiveIntegerField(verbose_name=_('display date format'), choices=DATE_LAYOUT, default=SHOW_ALL)

    number_layout = models.PositiveIntegerField(verbose_name=_('number layout format'), choices=NUMBER_LAYOUT, default=PERCENT)

    background_color = ColorField(verbose_name=_('background color'), default='#F8F8FF')
    basic_color = ColorField(verbose_name=_('basic color'), default='#ddd')
    diff_color = ColorField(verbose_name=_('differency color'), default='#B22222')
    progress_color = ColorField(verbose_name=_('progress color'), default='#228B22')

    @property
    def native_start_date(self):
        return self.start_date.replace(tzinfo=None)

    @property
    def native_end_date(self):
        return self.end_date.replace(tzinfo=None)

    class Meta:
        verbose_name = _('Chart of achievements')
        verbose_name_plural = _('achievement charts')

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_('Choose corrent date range'))

    def get_start_date(self):
        return self.start_date if self.date_layout != self.EMPTY else None

    def get_current_date(self):
        return datetime.now() if self.date_layout == self.SHOW_ALL else None

    def get_end_date(self):
        return self.end_date if self.date_layout != self.EMPTY else None

    def _get_progress(self, a, b):
        progress = float(a) / b * 100
        if progress > 100:
            return 100
        elif progress < 0:
            return 0
        else:
            return int(progress)

    def get_number_label(self):
        if self.pk:
            ammount = sum(self.currentprogress_set.values_list('ammount', flat=True))
            if self.number_layout == self.PERCENT:
                return '{}%'.format(self._get_progress(ammount, self.goal))
            elif self.number_layout == self.NUMBERS:
                return '{}/{}'.format(ammount, self.goal)
        return ''
    get_number_label.allow_tags = True
    get_number_label.short_description = _('current state')

    def get_progress_bar(self):
        ammount = sum(self.currentprogress_set.values_list('ammount', flat=True))
        now = datetime.now().replace(tzinfo=None)
        return {
            'currently': self._get_progress((now - self.native_start_date).total_seconds(), (self.native_end_date - self.native_start_date).total_seconds()),
            'ratio': self._get_progress(ammount, self.goal),
        }

    def preview(self):
        if self.pk:
            return mark_safe('''<div style="height:135px;width:500px;top:-1em;left:10em;position:relative;">
            <div id="get_progress_timeline" data-timeline="{}"></div><script type="text/javascript">init();</script>
            </div>'''.format(self.pk))
    preview.short_description = _('preview')



class CurrentProgress(models.Model):

    date = models.DateTimeField(verbose_name=_('date'), default=datetime.now, blank=True)
    ammount = models.IntegerField(verbose_name=_('new value'))
    progress_timeline = models.ForeignKey(ProgressTimeLine, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('current state')
        verbose_name_plural = _('current states')
