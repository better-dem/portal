web: gunicorn portal.wsgi
worker: celery worker -A portal
worker2: python worker.py
release: python manage.py migrate
