import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_library.settings')

app = Celery('django_library')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'send-return-reminders-daily': {
        'task': 'loans.tasks.send_return_reminders',
        'schedule': crontab(hour=5, minute=0),
    },
}
