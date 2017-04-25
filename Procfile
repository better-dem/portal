web: gunicorn portal.wsgi
worker: celery -A portal worker
long_jobs: celery -A portal worker -Q long_job --concurrency=1
beat: celery -A portal beat
release: python manage.py migrate --noinput && for f in `ls */fixed_data.json` ; do python manage.py loaddata $f ; done  && python manage.py collectstatic --noinput --clear && python manage.py compress
