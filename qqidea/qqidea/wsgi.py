"""
WSGI config for qqidea project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qqidea.settings')

#  读取 QQIDEA_PROFILE 环境变量，如果没有取默认值develop
profile = os.environ.get('QQIDEA_PROFILE','develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qqidea.settings.%s' % profile)

application = get_wsgi_application()
