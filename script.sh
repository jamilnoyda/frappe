#!/bin/sh


celery -A app.celery -l info --broker=redis://localhost:6379/0
celery -A app.celery beat -l info
flower -A app.celery --broker=redis://localhost:6379/0 --port=5555

