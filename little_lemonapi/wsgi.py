"""
WSGI config for little_lemonapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Update the DJANGO_SETTINGS_MODULE to point to your Django project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'little_lemonapi.settings')

# Create the WSGI application using get_wsgi_application
application = get_wsgi_application()
