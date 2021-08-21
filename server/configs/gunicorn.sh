#!/bin/bash

NAME="inventoryFEN"                              #Name of the application (*)
DJANGODIR=/media/main_storage/anupadkh/inventoryCMS    # Django project directory (*)
SOCKFILE=/media/main_storage/anupadkh/run/inventory.sock        # we will communicate using this unix socket (*)
USER=anupadkh                                       # the user to run as (*)
GROUP=anupadkh                                    # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=fEN.prod             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=fEN.wsgi                     # WSGI module name (*)
VENV_DIR=/media/main_storage/anupadkh/venv_inventory                      #VirtualEnv directory

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
# source /home/ppc/.bash_profile
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
