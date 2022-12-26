"""
ASGI config for qqidea project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qqidea.settings')

#  读取 QQIDEA_PROFILE 环境变量，如果没有取默认值develop
profile = os.environ.get('QQIDEA_PROFILE','develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qqidea.settings.%s' % profile)

application = get_asgi_application()
