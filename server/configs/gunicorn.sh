#!/bin/bash

NAME="portal"                              #Name of the application (*)
DJANGODIR=/home/ppc/deploy/GandakiProvinceData    # Django project directory (*)
SOCKFILE=/home/ppc/deploy/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=ppc                                        # the user to run as (*)
GROUP=ppc                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=configs.prod             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=configs.wsgi                     # WSGI module name (*)
VENV_DIR=/home/ppc/deploy/portal_venv                      #VirtualEnv directory

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source /home/ppc/.bash_profile
cd $DJANGODIR
source $VENV_DIR/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VENV_DIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
