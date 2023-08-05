=====
Progress Timeline
=====

TODO


Quick start
-----------

1. Add "progress_timeline" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'progress_timeline',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('progress-timeline/', include('progress_timeline.urls')),

3. Run `python manage.py migrate` to create the models.
