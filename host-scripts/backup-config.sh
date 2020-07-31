#!/bin/bash
# Creates a backup of the config directory
# Set this as a cron job and preferably sync the backup directory to cloud / reliable server
TIME=`date +%b-%d-%y`
FILENAME=backup-$TIME.tar.gz
SRCDIR=$(dirname "$0"})/../config
DESDIR=$(dirname "$0"})/../backups
BACKUPNAME="$DESDIR/$FILENAME"
mkdir -p $DESDIR
tar -cpzf $BACKUPNAME $SRCDIR
echo "Backed up $SRCDIR to $BACKUPNAME"