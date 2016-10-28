web: gunicorn portal.wsgi
worker: celery worker -A portal -B
release: python manage.py migrate
