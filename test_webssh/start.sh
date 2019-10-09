#!/bin/sh
/etc/init.d/cron start
python /app/manage.py crontab add
python /app/manage.py collectstatic --noinput
python /app/manage.py makemigrations --fake-initial --noinput
python /app/manage.py migrate app01 --fake-initial --noinput
