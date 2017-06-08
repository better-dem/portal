.. Linux installation

Linux Installation
==================

This document contains instructions to setup the Portal on Linux.
Most developers will find this unreasonably complicated and will prefer :doc:`developing_from_vm`.

.. contents::

Prerequisites
-------------

Heroku Command Line tool
++++++++++++++++++++++++

Download the heroku command line tool.

Install Python Pre-requisites
+++++++++++++++++++++++++++++

Using python 2.7, 

> sudo pip install -r requirements.txt

Environment Variables
+++++++++++++++++++++
  | DJANGO_SECRET_KEY=
  | DJANGO_DEBUG_STATE=
  | GOOGLE_MAPS_API_KEY=
  | EMAIL_HOST=
  | EMAIL_PORT=
  | EMAIL_ACCOUNT_NAME=
  | EMAIL_ACCOUNT_PASSWORD=
  | FROM_EMAIL=
  | REDIS_URL=redis://
  | SECURE_SSL_REDIRECT=
  | PREPEND_WWW=
  | FB_APP_ID=
  | SITE=
  | STRIPE_API_KEY=
  | STRIPE_PUBLISHABLE_KEY=
  | OPENSTATES_KEY=
  | AWS_ACCESS_KEY_ID=
  | AWS_SECRET_ACCESS_KEY=
  | AWS_STORAGE_BUCKET_NAME=
  | AWS_S3_REGION=

Setting up AWS static file storage and direct uploads
+++++++++++++++++++++++++++++++++++++++++++++++++++++

- Create a bucket
- add aws environment variables for a user that has full access to that bucket
- edit CORS configuration in bucket preferences to allow cross-site sharing with the app's url

Redis
+++++

Install redis-server, the server has to run for background jobs to work.


PostGIS 
++++++++

Install postgresql, postgis, and spatialite:

> sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 spatialite-bin postgresql-server-dev-9.3 python-psycopg2

Create portal database:
> createdb portal

> heroku pg:psql --app [app name]
>>> CREATE EXTENSION postgis;

Nunjucks
++++++++

> apt-get install nodejs-legacy npm
> npm install nunjucks

to pre-compile templates once they change, do:
> cd utils
> ./compile_nunjucks_templates.sh

This will modify core/static/core/js/templates.js , so we need to re-release in development

Building
--------

> heroku local release
