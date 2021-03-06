from __future__ import absolute_import
import celery.schedules
import os
import sys
import dj_database_url
from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ["DJANGO_DEBUG_STATE"]=="True"

# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'manual_news_article_curation.apps.ManualNewsArticleCurationConfig',
    'land_use_planning.apps.LandUsePlanningConfig',
    'city_budgeting.apps.CityBudgetingConfig',
    'tool_review.apps.ToolReviewConfig',
    'single_quiz.apps.SingleQuizConfig',
    'ballot_decider.apps.BallotDeciderConfig',
    'interactive_visualization.apps.InteractiveVisualizationConfig',
    'beat_the_bullshit.apps.BeatTheBullshitConfig',
    'legislators.apps.LegislatorsConfig',
    'reading_assignment.apps.ReadingAssignmentConfig',
    'widgets.apps.WidgetsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    's3direct',
    'compressor'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static'
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'portal',
    }
}

## Update database configuration with $DATABASE_URL.
# trying to use GIS database. Sortof following instructions from https://devcenter.heroku.com/articles/postgis
DATABASES['default'].update(dj_database_url.config())
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECURE_SSL_REDIRECT = os.environ["SECURE_SSL_REDIRECT"]=="True"
PREPEND_WWW = os.environ["PREPEND_WWW"]=="True"

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
### I re-define this later to point to the s3 bucket
### so that asset definition paths will point to the CDN
### # STATIC_URL = '/static/' 

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# s3direct options
def upload_filename(original_filename):
    """
    clean up problematic characters from uploaded filenames and "guarentee" uniqueness by adding a timestamp
    """
    ans = "uploads/file_uploads/"
    ans += ''.join([ch for ch in str(timezone.now()) if ch.isalnum() or ch in ["-", "."]])
    ans += '_'
    ans += ''.join([ch for ch in original_filename if ch.isalnum() or ch in ["-", "_", "."]])
    return ans

S3DIRECT_REGION = os.environ["AWS_S3_REGION"]
S3DIRECT_DESTINATIONS = {
    # destination specifically for uploading large administrative files
    'data_upload': {
        'key': lambda original_filename: 'uploads/misc/tmp',
        'auth': lambda u: u.is_authenticated()
    },
    'file_upload': {
        'key': lambda original_filename: upload_filename(original_filename),
        'auth': lambda u: u.is_authenticated() 
    }
}

# S3 static file storage with django-storages and django_compression

STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder','compressor.finders.CompressorFinder']
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'core.cached_s3_storage.CachedS3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
STATICFILES_STORAGE = 'core.cached_s3_storage.CachedS3BotoStorage'
AWS_S3_HOST="s3-{}.amazonaws.com".format(os.environ["AWS_S3_REGION"])
STATIC_URL = "https://{}.{}/".format(AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)
AWS_QUERYSTRING_AUTH = False    # there are to be no private files served from the bucket. 

### storages option which should be able to allow indefinite caching of never-stale static files
AWS_S3_OBJECT_PARAMETERS = {
    'Cache-Control': 'max-age=31536000', # 1 year, though it could be infinite
}

# django_compression settings
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = 'core.cached_s3_storage.CachedS3BotoStorage'
COMPRESS_ROOT = STATIC_ROOT

### Settings for django registration
ACCOUNT_ACTIVATION_DAYS=7
REGISTRATION_OPEN=True
REGISTRATION_SALT="fd43*7uHJjh(*Jmnbyt5$Th"

### Email information loaded from environment variables
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS=True
EMAIL_PORT=int(os.environ["EMAIL_PORT"])
EMAIL_HOST=os.environ["EMAIL_HOST"]
EMAIL_HOST_USER=os.environ["EMAIL_ACCOUNT_NAME"]
EMAIL_HOST_PASSWORD=os.environ["EMAIL_ACCOUNT_PASSWORD"]
SERVER_EMAIL=os.environ["EMAIL_ACCOUNT_NAME"]
DEFAULT_FROM_EMAIL=os.environ["FROM_EMAIL"]

### celery config
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
BROKER_URL = os.environ["REDIS_URL"]
CELERY_RESULT_BACKEND=BROKER_URL
CELERYD_TASK_SOFT_TIME_LIMIT=60
CELERY_REDIS_MAX_CONNECTIONS=1
BROKER_POOL_LIMIT=1
CELERYD_PREFETCH_MULTIPLIER=1

# from http://stackoverflow.com/questions/20116573/in-celery-3-1-making-django-periodic-task
CELERYBEAT_SCHEDULE = {
    'longjobs': {
        'task': 'core.tasks.pick_long_job',
        'schedule': celery.schedules.schedule(run_every=5),
    },
}
