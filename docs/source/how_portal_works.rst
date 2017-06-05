.. How Portal Works

How Portal Works
==================

This document describes the Better Democracy Portal's architecture at a high level so developers can jump in quickly.

.. contents::
   
Directory Structure
-------------------

This project uses a standard django project structure.
"portal" is the project name, so the portal sub-directory contains the standard settings.py and root urls conf files.

The "core" app contains view templates which all participation apps should make use of, and defines the base models all participation apps need to inherit from.

The configuration files: app.json, circle.yml, requirements.txt, runtime.txt, and Procfile all control various aspects of how environements are set up for this project when it is pushed to CircleCI and Heroku

  | ├── app.json
  | ├── circle.yml
  | ├── core
  | │   ├── models.py
  | │   ├── views.py
  | │   ├── tasks.py
  | │   ├── ...
  | │   └── urls.py
  | ├── docs
  | ├── <participation_app_1>
  | ├── <participation_app_2>
  | ├── <participation_app_3>
  | ├── ...
  | ├── manage.py
  | ├── portal
  | │   ├── celery.py
  | │   ├── settings.py
  | │   ├── ...
  | │   └── urls.py
  | ├── Procfile
  | ├── README.md
  | ├── requirements.txt
  | ├── runtime.txt
  | ├── utils
  | └── widgets

Participation Apps
------------------

Portal defines an interface whereby new apps can be incorporated into the same interface, allowing a uniform presentation for different types of participation activities.
TODO: this hasn't actually been completely formalized, see: https://github.com/better-dem/portal/issues/69

Each 'participation app' is a django app (created using heroku local:run manage.py startapp <appname>).

The main requirements to create a participation app are:
 - Implement (at least one) core.ParticipationProject subclass
 - Implement (at least one) core.ParticipationItem subclass
 - Implement the required views in views.py: new_project, administer_project, and participate
 - Add app metadata to apps.py
 - Install the app in the django project (settings.py), makemigrations, migrate the database

Major Requirements and What They Do
-----------------------------------

Background Tasks with Celery / Redis
++++++++++++++++++++++++++++++++++++

This app delegates background tasks using celery and redis.
This is required to make the app remain responsive, as described here: https://devcenter.heroku.com/articles/background-jobs-queueing .
Any app can create background tasks by following the core app's example.
Longer jobs should use the LongJobs API, which hasn't been documented yet! 
TODO Fix this: https://github.com/better-dem/portal/issues/70


When you need to get rid of the task queue and redis locks, try:

  | > heroku local:run celery -A portal purge
  | > redis-cli
  | >> flushdb



PostGIS 
+++++++

Portal's backing database is Postgres with GIS extensions.
We almost exclusively connect to this using the django ORM.

Bootstrap 3
+++++++++++

All of the Portal's style comes from Bootstrap 3.
The base template which the entire site inherits from can be found at core/templates/core/base.html , it includes a navbar and loads common javascript.
Several other templates which are used throughout the project can be found in the core templates folder, for example generic_form.html .

HTML Templates: Django + Nunjucks
+++++++++++++++++++++++++++++++++

Nunjucks is a library for client-side template rendering.
We use it for rendering content returned via AJAX.
TODO: finish switching all post-ajax rendering to Nunjucks https://github.com/better-dem/portal/issues/71

Most of the project's HTML is rendered from Django templates.
You will find these files under app_name/templates/app_name/<name of template>.html (that's right, repeat the app name in the path).
Unfortunately, these are hard to distinguish from Jinja 2 templates (used by Nunjucks), which are also stored in the same directories, so sometimes it's hard to tell whether you're editing a django template or a jinja template.

You can see the complete list of nunjucks templates hard-coded in utils/compile_nunjucks_templates.sh .

Local Development with Nunjucks
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Install nunjucks using Node:
  | > apt-get install nodejs-legacy npm
  | > npm install nunjucks

to pre-compile templates once they change, do:
  | > cd utils
  | > ./compile_nunjucks_templates.sh

This will modify core/static/core/js/templates.js , so we need to re-release:
  | > heroku local release

Javascript and CSS Compression
++++++++++++++++++++++++++++++

We compress javascript and CSS in development and in production, so when you modify a .js file, you need to push the compressed version to S3.
Do this with:

  | > heroku local release

Administering the Portal
------------------------

There are several tools for administering the Portal.
Some work through the command line, ex:

  | > heroku local:run python manage.py authorize_user -u <username> --participationapp <app name>

Others are done through the graphical interface.
All of these views can be accessed from the profile view of an authorized user.

Adding Content to the Portal
++++++++++++++++++++++++++++

Content is added through the Journalist, Teacher, or User Profile interfaces (or as a background task in the case of openstates).
Go to your profile, then click "Create ____" for one of the content types for an example of this.

