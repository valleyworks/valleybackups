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

AWS Glacier set up
------------------

Create access_key and secret_access_key in AWS Console
......................................................

* Go to https://console.aws.amazon.com/iam/
* Create a new user valleybackups
* Then click on show user credentials
* Download the credentials

Get the AWS account id:
.......................

* Go to https://console.aws.amazon.com/billing/home?#/account
* Copy the account id

Get the AWS region:
...................

* Go to Management Console and get the region string from the url, example: https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2

Set permissions in AWS
......................

* Go to IAM users https://console.aws.amazon.com/iam/home?region=us-west-2#users
* Go to the user created (valleybackups)
* Click on Permissions
* Click on Attach Policy
* Look for Glacier and SNS
* Click on AmazonGlacierFullAccess and then AmazonSNSFullAccess
* Click on Attach Policy

Create a Glacier Vault:
.......................

* Go to https://us-west-2.console.aws.amazon.com/glacier/home?region=us-west-2#/initial-start and click on Get Started
* Choose a name and click next, for example **"mybackups"**
* Choose Enable notifications and create a new SNS topic
* Choose a Topic Name: **mybackupsnotification**
* Check both Archive Retrieval and Vault Inventory options
* Click Next then Submit

Set the configuration in ValleyBackups
......................................

* ``valleybackups set_config base access_key_id *<access_key>*``
* ``valleybackups set_config base secret_access_key *<secret_access_key>*``
* ``valleybackups set_config base aws_account_id *<account_id>*``
* ``valleybackups set_config base region_name *us-west-2*``
* ``valleybackups set_config glacier vault_name *mybackups*``

Verify config:
..............

* valleybackups get_config

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


How to use it
-------------


Pick any file you want to backup and push it to AWS Glacier:
    ``valleybackups backup <filename>``

Then list all your backed up files:
    ``valleybackups list``

Retrieve a file from valleybackups by using the ID in the previous list:
    ``valleybackups request 1``

This will generate a job to retrieve the file. It will usually takes hour. Once it’s ready you can retrieve in the folder you currently are by running:
    ``valleybackups download 1``


Available Commands
------------------

Backup
......

Run ``valleybackups backup <file>``

Batch Upload
............

Run ``valleybackups bacth_upload <folder>``

List Archives
.............

Run ``valleybackups list``

Request file
............

Run ``valleybackups request <id>`` (id is listed on list_files command)

List Uncompleted (Pending) Jobs
...............................

Run ``valleybackups list_uncompleted_jobs``

Check Config
............

Run ``valleybackups check_config``

Download File
.............

Run ``valleybackups download <job_id>`` (This id is returned by SNS)

Create Vault
............

Run ``valleybackups create_vault <vault_name>``


Support
=======

Need help installing ValleyBackups in your project? Contact us via http://www.valleyworks.us/contact/ or email us to valleybackups@valleyworks.us.
