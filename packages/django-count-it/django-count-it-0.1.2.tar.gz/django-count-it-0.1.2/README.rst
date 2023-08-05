=====
Counter
=====

Counter is a simple Django app to create counters. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "counter" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'counter',
    ]

2. Run `python manage.py migrate` to create the counter models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a counter (you'll need the Admin app enabled).
