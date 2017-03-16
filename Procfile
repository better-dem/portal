web: gunicorn portal.wsgi
worker: celery worker -A portal -B
release: python manage.py migrate --noinput && for f in `ls */fixed_data.json` ; do python manage.py loaddata $f ; done  && python manage.py collectstatic --noinput --clear && python manage.py compress
