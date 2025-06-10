"""
WSGI config for HivePulse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from HivePulse.settings import DEBUG
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HivePulse.settings')

if not DEBUG:
    application = Cling(get_wsgi_application())
else:
    application = get_wsgi_application()
