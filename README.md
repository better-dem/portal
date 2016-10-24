# Better Dem Portal

Created using the [Heroku django starter template](https://github.com/heroku/heroku-django-template/)

## Environment Variables

DJANGO_SECRET_KEY=
DJANGO_DEBUG_STATE=
GMAIL_ACCOUNT_NAME=
GMAIL_ACCOUNT_PASSWORD=

## Setting up GIS database to reun locally

Install postgresql, postgis, and spatialite:

sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 spatialite-bin postgresql-server-dev-9.3 python-psycopg2


Create a postgresql user with your username:

> sudo su postgres
> createuser --interactive -P
Enter name of role to add: portal
Enter password for new role: (portal)
Enter it again: (portal)
Shall the new role be a superuser? (y/n) y

Create portal database:
> createdb portal_gis_db

