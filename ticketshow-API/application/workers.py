from celery import Celery 
from flask import current_app as app

celery_app = Celery('Application jobs')

