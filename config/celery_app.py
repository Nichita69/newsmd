from os import environ
from time import sleep
from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, track_started=True)
def debug_task(self, sleep_seconds: int = 0, raise_exception: bool = False):
    if sleep_seconds:
        sleep(sleep_seconds)

    if raise_exception:
        raise Exception("Intentional exception!")

    print('Request: {0!r}'.format(self.request))
