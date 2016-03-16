# glacierbackups
A Backup tool with AWS Glacier support

## Installation

* From the project's root folder run `virtualenv .` to create a jailed environment for this script. 

* Run `source bin/activate` and `pip install -r requirements.txt` to install dependencies.

* Grant execution permissions to `valleybackups.sh` with the command `chmod +x valleybackups.sh`

* Finally, make a symbolic link. For example: `ln -s /opt/glacierbackups/valleybackups.sh /usr/bin/valleybackups`

## Configuration

Place a file called ***valleybackups.conf*** with the following content:

```
[base]

ACCESS_KEY_ID=...
SECRET_ACCESS_KEY=...
AWS_ACCOUNT_ID=...

[glacier]

VAULT_NAME=...

```

## Usage

Run `valleybackups backup <file>`
