# -*- coding: utf-8 -*-

import random
import string

from datetime import datetime

from django import template

from progress_timeline.models import ProgressTimeLine


register = template.Library()


@register.inclusion_tag("progress_timeline/progresstimeline_detail.html")
def get_progress_timeline(object_id):
    try:
        progress_timeline = ProgressTimeLine.objects.get(pk=object_id)
    except ProgressTimeLine.DoesNotExist:
        return {}
    else:
        context = progress_timeline.get_progress_bar()
        context["object"] = progress_timeline
        return context
