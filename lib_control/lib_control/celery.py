import os

from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib_control.settings')

app = Celery('lib_control', broker='redis://localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def set_fine():
    pass
