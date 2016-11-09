from __future__ import absolute_import
import celery.schedules
import os
import dj_database_url

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
    'dummy_participation_project.apps.DummyParticipationProjectConfig',
    'manual_news_article_curation.apps.ManualNewsArticleCurationConfig',
    'land_use_planning.apps.LandUsePlanningConfig',
    'city_budgeting.apps.CityBudgetingConfig',
    'widgets.apps.WidgetsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # use the storages app
    'storages',
    's3direct'
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
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'portal',
    }
}

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

## Update database configuration with $DATABASE_URL.
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# trying to use GIS database. Sortof following instructions from https://devcenter.heroku.com/articles/postgis
DATABASES['default'].update(dj_database_url.config())
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

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
S3DIRECT_REGION = 'us-west-1'
S3DIRECT_DESTINATIONS = {
    # destination specifically for uploading large administrative files
    'data_upload': {
        'key': lambda original_filename: 'uploads/misc/tmp',
        'auth': lambda u: u.is_authenticated() 
    }
}

# S3 static file storage with django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_HOST="s3-us-west-1.amazonaws.com"
STATIC_URL = "https://"+AWS_STORAGE_BUCKET_NAME+"."+AWS_S3_HOST+"/"

### Settings for django registration
ACCOUNT_ACTIVATION_DAYS=2
REGISTRATION_OPEN=True
REGISTRATION_SALT="fd43*7uHJjh(*Jmnbyt5$Th"

### Email information loaded from environment variables
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER=os.environ["GMAIL_ACCOUNT_NAME"]
EMAIL_HOST_PASSWORD=os.environ["GMAIL_ACCOUNT_PASSWORD"]
SERVER_EMAIL=os.environ["GMAIL_ACCOUNT_NAME"]
DEFAULT_FROM_EMAIL="Better Dem Portal"

### celery config
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
BROKER_URL = os.environ["REDIS_URL"]

# from http://stackoverflow.com/questions/20116573/in-celery-3-1-making-django-periodic-task
CELERYBEAT_SCHEDULE = {
    # 'item-update': {
    #     'task': 'core.tasks.item_update',
    #     'schedule': celery.schedules.schedule(run_every=2)
    # },
}
