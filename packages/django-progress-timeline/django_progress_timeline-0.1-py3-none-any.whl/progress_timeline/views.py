from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import ProgressTimeLine


class ProgressTimeLineDetailView(DetailView):
    model = ProgressTimeLine

    def get_basic_color(self):
        basic_color = self.request.GET.get('basic_color')
        return '#{}'.format(basic_color) if basic_color else  self.object.basic_color

    def get_progress_color(self):
        progress_color = self.request.GET.get('progress_color')
        return '#{}'.format(progress_color) if progress_color else self.object.progress_color

    def get_diff_color(self):
        diff_color = self.request.GET.get('diff_color')
        return '#{}'.format(diff_color) if diff_color else self.object.diff_color

    def get_background_color(self):
        background_color = self.request.GET.get('background_color')
        return "#{}".format(background_color) if background_color else self.object.background_color

    def get_context_data(self, **kwargs):
        context = super(ProgressTimeLineDetailView, self).get_context_data(**kwargs)
        context['basic_color'] = self.get_basic_color()
        context['progress_color'] = self.get_progress_color()
        context['diff_color'] = self.get_diff_color()
        context['background_color'] = self.get_background_color()
        context.update(self.object.get_progress_bar())
        return context
