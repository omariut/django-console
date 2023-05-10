# CodeLess-Django

CodeLess-Django is a Django app to develop django apps without writing code. Developers can create apps and models from a web page where all the models field types and options are placed in front of developers eyes . CodeLess-Django will take care of adding apps to settings file, creating generic views and api views etc.
Detailed documentation is in the "docs" directory.

## Quick start
-----------

1. Add "codeless-django" to your INSTALLED_APPS setting like this::
``` python
    INSTALLED_APPS = [
        ...
        'codeless_django',
    ]
```

2. Include the polls URLconf in your project urls.py like this::
``` python

    path('codeless-django/', include('codeless_django.urls')),
```


3. Start the development server and visit http://127.0.0.1:8000/codeless-django/ to create apps and models.
