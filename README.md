# Better Dem Portal

Created using the [Heroku django starter template](https://github.com/heroku/heroku-django-template/)

## Project Structure

Some of the most important basics are shown here:

```
├── app.json
├── circle.yml
├── core
├── dummy_participation_project
├── land_use_planning
├── manage.py
├── manual_news_article_curation
├── portal
│   ├── celery.py
│   ├── settings.py
│   └── urls.py
├── Procfile
├── requirements.txt
├── runtime.txt
└── widgets
```

At a high level, this is a standard django project structure.
"Portal" is the project name, so the portal sub-directory contains the standard settings.py and root urls conf files.

### Core app
The core app contains view templates which all participation apps should make use of, and defines the base models all participation apps need to inherit from.

### Participation Apps
Portal defines an interface whereby new apps can be incorporated into the same interface, allowing a uniform presentation for different types of participation activities.

Existing participation apps in the current project are: dummy_participation_project, land_use_planning, and manual_news_article_curation.
Each 'participation app' is a django app (created using heroku local:run manage.py startapp <appname>).

The main requirements of a participation app are:
* Install the app in the django project (settings.py), makemigrations, migrate the database
* Create a project model which inherits (directly) from core.ParticipationProject
..* Importantly, override this model's methods. See existing participation apps for examples
* Create a participation item model which inherits (directly) from core.ParticipationItem
..* Importantly, override this model's methods. See existing participation apps for examples
* Implement the required views in views.py: new_project, administer_project, and participate
* register the app with core in apps.py (ooverride the apps.XXXXConfig.ready() method)

### Continuous deployment files
app.json, circle.yml, requirements.txt, runtime.txt, and Procfile all control various aspects of how environements are set up for this project when it is pushed to CircleCI and Heroku

### Celery
This app delegates background tasks using celery and redis.
This is required to make the app remain responsive, as described [here](https://devcenter.heroku.com/articles/background-jobs-queueing).
Any app can create background tasks by following the core app's example.


## Running The App

### Environment Variables

DJANGO_SECRET_KEY=
DJANGO_DEBUG_STATE=
GMAIL_ACCOUNT_NAME=
GMAIL_ACCOUNT_PASSWORD=
GOOGLE_MAPS_API_KEY=
REDIS_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

### Setting up AWS static file storage and direct uploads

 - Create a bucket
 - add aws environment variables for a user that has full access to that bucket
 - edit CORS configuration in bucket preferences to allow cross-site sharing with the app's url

### Setting up Redis

#### Locally
Install redis-server, the server has to run for background jobs to work.


#### On heroku
Redis is one of the officially supported addons, add it on.



### Setting up GIS 

#### GIS database to run locally

Install postgresql, postgis, and spatialite:

> sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 spatialite-bin postgresql-server-dev-9.3 python-psycopg2

Create portal database:
> createdb portal

#### Setting up GIS database for CircleCI

automated. See circle.yml

#### Setting up GIS database for Heroku

lots is automated, see portal/settings.py, core/models.py

#### GDAL:

I use the heroku-geo-buildpack buildpack
Its URL is: https://github.com/cyberdelia/heroku-geo-buildpack.git
I manually set these buildacks from heroku, which seems to ignore app.json?
 - At least for the review apps

#### Postgres:

> heroku pg:psql --app [app name]
>>> CREATE EXTENSION postgis;
>>> [ctrl-D]


### Setting up the initial data
 - see Procfile's release steps, these include loading data fixtures for any participation apps that have them
 - create a user (by visiting the site)
 - add core app priviledges for that user:
> heroku local:run python manage.py authorize_user -u <username> --participationapp core

The rest is done from the /upload_dataset page

 - upload usa_states: format: usa_and_states_v0
 - upload us cities (Requires us-cities which can be bought from uscitieslist.org): format: uscitieslist_csv_v0

Confirm state is reasonable by going to /tags


