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

    url(r'^progress_timeline/', include('progress_timeline.urls')),

3. Run `python manage.py migrate` to create the models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).


