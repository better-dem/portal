# Better Dem Portal

Created using the [Heroku django starter template](https://github.com/heroku/heroku-django-template/)

## Environment Variables

DJANGO_SECRET_KEY=
DJANGO_DEBUG_STATE=
GMAIL_ACCOUNT_NAME=
GMAIL_ACCOUNT_PASSWORD=

## Setting up GIS database to run locally

Install postgresql, postgis, and spatialite:

sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 spatialite-bin postgresql-server-dev-9.3 python-psycopg2

Create portal database:
> createdb portal

## Setting up GIS database for CircleCI

automated. See circle.yml

## Setting up GIS database for Heroku

lots is automated, see portal/settings.py, core/models.py

> heroku pg:psql --app [app name]
>>> CREATE EXTENSION postgis;
>>> [ctrl-D]

## Setting up geo tags

Requires us-cities which can be bought from uscitieslist.org

Example command to set up geo tags for cities:

heroku local:run python manage.py pull_and_add_osm_data -u http://download.geofabrik.de/north-america/us/delaware-latest.osm.bz2
