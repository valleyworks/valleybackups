Welcome to ValleyBackups's documentation!
=========================================

Contents:

.. toctree::
    :maxdepth: 2

    howitworks
    api/index


Installation
------------

* From the project's root folder run ``pip install --editable`` to install the package and its dependencies.

* The app will be available with the command ``valleybackups``

Configuration
-------------

* Check current configuration: ``valleybackups check_config``

* Setting configuration values: ``valleybackups set_config <section> <setting> <value``, for ex: ``valleybackups set_config glacier vault_name glacier_backups_1``


Available Commands
-----

Boot-up server (for sns notifications)
.....................................

This server listens to SNS notifications, and triggers file downloads when a requested file is ready.

Run ``valleybackups run_sns_listener``

Backup
......

Run ``valleybackups backup <file>``

Batch Upload
............

Run ``valleybackups bacth_upload <folder>``

List Archives
.............

Run ``valleybackups list_files``

Request file
............

Run ``valleybackups request_file <id>`` (id is listed on list_files command)

List Uncompleted (Pending) Jobs
...............................

Run ``valleybackups list_uncompleted_jobs``

Check Config
............

Run ``valleybackups check_config``

Download File
.............

Run ``valleybackups download_file <job_id>`` (This id is returned by SNS)

Create Vault
............

Run ``valleybackups create_vault <vault_name>``
