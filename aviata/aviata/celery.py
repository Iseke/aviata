import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aviata.settings")

app = Celery("aviata")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = 'Asia/Almaty'

app.conf.beat_schedule = {
    'update_every_24_hour': {
        'task': 'api.tasks.take_directions',
        'schedule': crontab(hour=0, minute=0)
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))