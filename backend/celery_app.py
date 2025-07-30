from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    celery.conf.update({
        'broker_url': app.config['CELERY_BROKER_URL'],
        'result_backend': app.config['CELERY_RESULT_BACKEND'],
        'timezone': app.config.get('CELERY_TIMEZONE', 'Asia/Kolkata'),
        'enable_utc': app.config.get('CELERY_ENABLE_UTC', False),
    })

    celery.conf.beat_schedule = {
        'send-daily-reminders': {
            'task': 'celery_tasks.daily_reminder.send_daily_reminders',
            'schedule': crontab(hour=5, minute=27),
        },
        'send-monthly-report': {
            'task': 'celery_tasks.monthly_report.send_monthly_report',
            'schedule': crontab(day_of_month=30, hour=5, minute=26),
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
