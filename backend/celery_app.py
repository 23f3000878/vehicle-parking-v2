from flask import Flask
from extensions import celery

def make_celery(app):
    celery.conf.update({
    'broker_url': app.config['CELERY_BROKER_URL'],
    'result_backend': app.config['CELERY_RESULT_BACKEND'],
    'beat_schedule': app.config.get('CELERY_BEAT_SCHEDULE', {}),
    'beat_scheduler': 'celery.beat.Scheduler',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
})


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery