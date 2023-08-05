from django.conf.urls import url

from .views import ProgressTimeLineDetailView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', ProgressTimeLineDetailView.as_view(), name='progress-detail'),
    url(r'^(?P<pk>[0-9]+)/$', ProgressTimeLineDetailView.as_view(), name='progress-detail'),
]
