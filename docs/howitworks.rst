How it Works
============

After a file is backed up in Glacier, a reference is stored in a local database.
This can be used for future retrievals with the command ``request_file``.

After this is done, a job is created in glacier (lasting aprox 4 hours), when this job is completed, AWS sends a request
to our sns endpoint (``run_sns_listener``) previously configured on AWS dashboard.


Our listener receives the AWS response, and then proceeds to download the file.
