.. Developing from Virtual Machine

Developing from Virtual Machine
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

For most developers, configuring the environment to run this app will be too burdensome.
This is why we provide a virtual machine for developers with much simpler setup requirements.

Setup
-----

Run the Virtual Machine
+++++++++++++++++++++++

- install Oracle VirtualBox for your host system
- download the developer VM image
- (optional) install guest additions. This allows the VM to adjust screen size and to be generally more usable.

Configure S3 development bucket
+++++++++++++++++++++++++++++++

Environment variables for the project are in ~/portal/.env , where they are already filled with default values.
However, some variables related to AWS simple storage need to be filled with your information.

- Go to AWS's S3 dashboard
- Create a bucket
- add aws environment variables for a user that has full access to that bucket
- edit CORS configuration in bucket preferences to allow cross-site sharing with the app's url

The environment variables you are setting should be:
`AWS_ACCESS_KEY_ID=`
`AWS_SECRET_ACCESS_KEY=`
`AWS_STORAGE_BUCKET_NAME=`

Configuring Other Features
++++++++++++++++++++++++++

Several features aren't described here, and don't need to be configured in many cases.
These include interactions with the Stripe, email, and Facebook APIs.

Running The Project
-------------------

Building the Project
++++++++++++++++++++

The project is located in ~/portal

> cd ~/portal
> heroku local release

The output will end with "Exited Succesfully" when the server has connected to S3 to upload static files, etc.


Running the Development Server
++++++++++++++++++++++++++++++

> cd ~/portal
> heroku local

You should now be able to visit the site in your browser at localhost:5000/
A superuser for the site already exists, username betterdem, password betterdem.

Contributing to the Project
---------------------------

This project is hosted on github, so you will need a github account.
- You will want to be logged in locally so that your commits are credited to you, not annonymous.
- To develop new features, work from a branch which branches from dev. we use an approach like the one here: http://nvie.com/posts/a-successful-git-branching-model/ .
- Create a pull request from your branch into dev when you think your features are ready
