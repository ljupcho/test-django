from __future__ import absolute_import, unicode_literals

import os
from celery import Celery, platforms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

celery_app = Celery('todo')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()