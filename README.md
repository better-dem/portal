# Better Dem Portal

Created using the [Heroku django starter template](https://github.com/heroku/heroku-django-template/)

## Environment Variables

DJANGO_SECRET_KEY=
DJANGO_DEBUG_STATE=
GMAIL_ACCOUNT_NAME=
GMAIL_ACCOUNT_PASSWORD=
REDIS_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

## Setting up AWS static file storage and direct uploads


## Setting up Redis

### Locally
Install redis-server, the server has to run for background jobs to work.


### On heroku
Redis is one of the officially supported addons, add it on.



## Setting up GIS 

### GIS database to run locally

Install postgresql, postgis, and spatialite:

sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 spatialite-bin postgresql-server-dev-9.3 python-psycopg2

Create portal database:
> createdb portal

### Setting up GIS database for CircleCI

automated. See circle.yml

### Setting up GIS database for Heroku

lots is automated, see portal/settings.py, core/models.py

### GDAL:

I use the heroku-geo-buildpack buildpack
Its URL is: https://github.com/cyberdelia/heroku-geo-buildpack.git
I manually set these buildacks from heroku, which seems to ignore app.json?
 - At least for the review apps

### Postgres:

> heroku pg:psql --app [app name]
>>> CREATE EXTENSION postgis;
>>> [ctrl-D]


### Uploading up geo tags

Requires us-cities which can be bought from uscitieslist.org

 - login with a user authorized to manage the core app
 - use: uscitieslist_csv_v0 for format id
 - upload your cities list csv file
 - work will be done in the background, check progress by visiting /tags view
