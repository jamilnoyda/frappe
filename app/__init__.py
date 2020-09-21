import logging

from flask import Flask
from celery import Celery
from flask_appbuilder import AppBuilder, SQLA

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)
from redis import Redis

import os
app.config["SESSION_REDIS"] = Redis(host="redis", port="6379")
r =app.config["SESSION_REDIS"]
# celery = Celery(app.name, broker=os.getenv('CELERY_BROKER_URL'))
# celery.conf.update(app.config)

# basedir = app.config.get('basedir')

celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
)
  
celery.config_from_object(app.config.from_object("config"))
TaskBase = celery.Task
# import subprocess
# import os
# import sys

# arg1=sys.argv[1]
# arg2=sys.argv[2]

# shell_command = basedir+'script.sh' + arg1 + ' '+ arg2
# P = subprocess.Popen(shell_command.split())
# P.wait()
"""






from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
