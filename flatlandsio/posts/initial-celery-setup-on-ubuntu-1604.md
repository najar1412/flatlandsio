This guide is originally from [pythad.github.io](https://pythad.github.io/articles/2016-12/how-to-run-celery-as-a-daemon-in-production). Full credit goes to them, this is just a condensed version for my reference.

### Introduction

Minimal needed to get [celery](http://www.celeryproject.org/) up and running in a venv on ubuntu.


### Init-script: celeryd

Create /etc/init.d/celeryd with the contents from https://github.com/celery/celery/blob/master/extra/generic-init.d/celeryd.

```
$ sudo nano /etc/init.d/celeryd
```

Finally, make it executable.

```
$ sudo chmod 755 /etc/init.d/celeryd
$ sudo chown root:root /etc/init.d/celeryd
```

### Configuration

Create /etc/default/celeryd and configure with contents below.

```
$ sudo nano /etc/default/celeryd
```

```
CELERY_BIN="project/venv/bin/celery"

# App instance to use.
CELERY_APP="project_django_project"

# Where to chdir at start.
CELERYD_CHDIR="/home/username/project/"

# Extra command-line arguments to the worker.
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log" CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
# You need to create this user manually (or you can choose
# a user/group combination that already exists (e.g., nobody).
CELERYD_USER="username" CELERYD_GROUP="username"

# If enabled pid and log directories will be created if missing, # and owned by the userid/group configured.
CELERY_CREATE_DIRS=1

export SECRET_KEY="foobar"
```

### Worker Management

```
$ sudo /etc/init.d/celeryd start
$ sudo /etc/init.d/celeryd status
$ sudo /etc/init.d/celeryd stop
```