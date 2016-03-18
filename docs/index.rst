.. ValleyBackups documentation master file, created by
   sphinx-quickstart on Fri Mar 18 12:56:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ValleyBackups's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2
   
   howitworks.rst
   db.rst
   glacier.rst


Installation
------------

* From the project's root folder run ``virtualenv .`` to create a jailed environment for this script. 

* Run ``source bin/activate`` and ``pip install -r requirements.txt`` to install dependencies.

* Grant execution permissions to ``valleybackups.sh`` with the command ``chmod +x valleybackups.sh``

* Finally, make a symbolic link. For example: ``sudo ln -s /opt/glacierbackups/valleybackups.sh /usr/bin/valleybackups``

Configuration
-------------

Place a file called **valleybackups.conf** with the following content:

    [base]

    ACCESS_KEY_ID=...

    SECRET_ACCESS_KEY=...

    AWS_ACCOUNT_ID=...

    [glacier]

    VAULT_NAME=...


Usage
-----

Bootup server (for sns notifications)
.....................................

This server listens to SNS notifications, and triggers file downloads when a requested file is ready.

Run ``supervisord`` to start the process watcher
Run ``supervisorctl status`` to check if the server is RUNNING

Backup
......

Run ``valleybackups backup <file>``

List Archives
.............

Run ``valleybackups list-files``

Request file
............

Run ``valleybackups request-file <id>`` (id is listed on list-files command)

List Uncompleted (Pending) Jobs
...............................

Run ``valleybackups list-uncompleted-jobs``
