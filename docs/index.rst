Welcome to ValleyBackups's documentation!
=========================================

Contents:

.. toctree::
    :maxdepth: 2

    howitworks
    api/index

Command-line based backup tool integrated with AWS Glacier

Installation
------------

* Run ``pip install valleybackups``.

Configuration
-------------

* Check current configuration: ``valleybackups check_config``

* Setting configuration values: ``valleybackups set_config <section> <setting> <value``, for ex: ``valleybackups set_config glacier vault_name glacier_backups_1``

Setting up your AWS account
---------------------------

**ACCOUNT ID**

* Login to your AWS Console and go to "My Account" (https://console.aws.amazon.com/billing/home#/account) and take note of your **Account ID**

**REGION NAME**

* Navigate to the Glacier service and take note of the current Region (easiest way is to look your current URL, for ex: https://us-west-2.console.aws.amazon.com, **Region** would be *us-west-2*

**ACCESS KEYS**

* Navigate to the IAM service -> Users -> *Create new User*

* Take note of the credentials shown

Creating a Glacier Vault
........................

* Run ``valleybackups create_vault <vault_name>`` (this process creates a SNS topic and assigns it to the recently created vault, to enable Notifications)


Create Notification Subscriptions for our Vault
...............................................

When we want to download any file stored in our Vault, we will need to configure a Subscription (basically telling AWS where to notify our app that the file is ready)

* Head to the SNS service on your AWS Console

* In **Topics** choose your recently created Topic (the name is <vault_name>Notification)

* Click on **Create Subscription**

* Follow instructions on http://docs.aws.amazon.com/sns/latest/dg/SubscribeTopic.html


Available Commands
------------------

Boot-up server (for sns notifications)
......................................

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
