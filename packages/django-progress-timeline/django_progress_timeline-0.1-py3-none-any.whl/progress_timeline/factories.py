from datetime import datetime, timedelta

from .models import ProgressTimeLine

import factory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyDateTime


class ProgressTimeLineFactory(factory.Factory):

    class Meta:
        model = ProgressTimeLine

    title = FuzzyText(length=12)
    description = FuzzyText(length=12)
    goal = FuzzyInteger(0, 42)

    start_date = datetime.now() - timedelta(days=10)
    end_date = datetime.now() + timedelta(days=10)
