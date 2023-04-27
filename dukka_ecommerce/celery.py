from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukka_ecommerce.settings')

app = Celery('dukka_ecommerce')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    #Scheduler Name
    'charge_customer_every_week': {
        # Task Name (Name Specified in Decorator)
        'task': 'charge_customer',  
        # Schedule      
        'schedule': crontab(0, 0, day_of_week='1'), #runs every first day of the week
        'options': {
            'expires': 15.0, #cancel task if not able to run after these seconds
        },
    },
    'charge_customer_every_month': {
        # Task Name (Name Specified in Decorator)
        'task': 'charge_customer',  
        # Schedule      
        'schedule': crontab(0, 0, day_of_month='1'),  #runs every first day of the month
        'options': {
            'expires': 15.0, #cancel task if not able to run after these seconds
        },
    },
       'charge_customer_every_year': {
        # Task Name (Name Specified in Decorator)
        'task': 'charge_customer',  
        # Schedule      
        'schedule': crontab(0, 0, month_of_year='1'), #runs every first month of the year
        'options': {
            'expires': 15.0, #cancel task if not able to run after these seconds
        },
    },

}