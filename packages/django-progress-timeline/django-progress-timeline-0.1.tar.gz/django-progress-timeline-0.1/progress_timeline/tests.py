# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from mock import patch

from django.test import TestCase

from progress_timeline.factories import ProgressTimeLineFactory
from progress_timeline.models import ProgressTimeLine
from progress_timeline.templatetags.progress_timeline_tags import get_progress_timeline


class ProgressTimeLineTest(TestCase):

    def test__get_progress(self):
        obj = ProgressTimeLineFactory.build()
        # first param, second param, result
        testing_data = [
            (0, 100, 0),
            (-1, 100, 0),
            (1, 100, 1),
            (25, 10, 100),
            (2, 5, 40),
            (1,3, 33),
        ]
        for data in testing_data:
            self.assertEqual(obj._get_progress(data[0], data[1]), data[2])

    def test_get_start_date_empty(self):
        obj = ProgressTimeLineFactory.build(date_layout=ProgressTimeLine.EMPTY)
        self.assertEqual(obj.get_start_date(), None)

    def test_get_start_date(self):
        obj = ProgressTimeLineFactory.build(date_layout=ProgressTimeLine.ONLY_EDGE)
        self.assertEqual(obj.get_start_date(), obj.start_date)

    def test_get_current_date_empty(self):
        obj = ProgressTimeLineFactory.build(date_layout=ProgressTimeLine.ONLY_EDGE)
        self.assertEqual(obj.get_current_date(), None)

    def test_get_end_date_empty(self):
        obj = ProgressTimeLineFactory.build(date_layout=ProgressTimeLine.ONLY_EDGE)
        self.assertEqual(obj.get_end_date(), obj.end_date)

    def test_get_end_date(self):
        obj = ProgressTimeLineFactory.build(date_layout=ProgressTimeLine.EMPTY)
        self.assertEqual(obj.get_current_date(), None)

    def test_get_progress_bar(self):
        testing_data = [
            (100, 0, 100),
            (100, 100, 50),
            (100, 50, 66),
            (10, 1, 90),
            (1, 10, 9),
            (1, 99, 1),
            (1, 100, 0)
        ]
        for data in testing_data:
            obj = ProgressTimeLineFactory.build(
                start_date=datetime.now() - timedelta(days=data[0]),
                end_date=datetime.now() + timedelta(days=data[1]))
            result = obj.get_progress_bar()
            self.assertEqual({'ratio': 0, 'currently': data[2]}, result)


class GetProgressTimelineTemplatetagTest(TestCase):

    @patch.object(ProgressTimeLine, 'objects')
    def test_get_progress_timeline(self, mock_objects):
        obj = ProgressTimeLineFactory.build(
            start_date=datetime.now() - timedelta(days=100),
            end_date=datetime.now() + timedelta(days=100))

        mock_objects.get.return_value = obj

        result = get_progress_timeline(obj.id)
        self.assertEqual({'ratio': 0, 'currently': 50, 'object': obj}, result)

    @patch.object(ProgressTimeLine, 'objects')
    def test_get_progress_timeline_without_object(self, mock_objects):
        mock_objects.get.side_effect = ProgressTimeLine.DoesNotExist
        result = get_progress_timeline(1)
        self.assertEqual({}, result)
