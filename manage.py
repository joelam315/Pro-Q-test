#!/usr/bin/env python
import os
import sys
import redis
from redis import ConnectionError
import logging
import subprocess

logging.basicConfig()
logger = logging.getLogger('redis')

rs = redis.Redis("localhost")
try:
    rs.ping()
except ConnectionError:
    logger.warning("Redis isn't running. trying to start redis server")
    subprocess.Popen(["redis-server"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    logger.info("Redis start successful")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
    os.environ['DJANGO_SETTINGS_MODULE'] = "crm.settings"
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            pass

        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
