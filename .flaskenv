FLASK_APP=run.py
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"



CSRF_ENABLED = True
FLASK_ENV=production
FLASK_ENV=development
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



# Flask-Mail configuration
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'JAMIL'
MAIL_PASSWORD ='JAMIL'
MAIL_DEFAULT_SENDER= 'jamilnoyda@gmail.com'


AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_KEY'

region=us-east-1
region_name = ''