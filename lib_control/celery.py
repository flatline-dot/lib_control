import os
import lib_app

from datetime import date
from celery import Celery
from django.db import IntegrityError, transaction


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib_control.settings')

app = Celery('lib_control', broker='redis://localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def set_fine():
    reading = lib_app.models.Reading.objects.all()
    for read in reading:
        if date.today() > read.date_return():
            try:
                with transaction.atomic():
                    fine = lib_app.models.Fine(user_id=read.user_id, reading_id=read, pay_status=False)
                    fine.save()
            except IntegrityError:
                print('Штраф уже выписан')
    return 'Проверка завершена'
