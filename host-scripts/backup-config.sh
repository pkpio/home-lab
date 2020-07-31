#!/bin/bash
# Creates a backup of the config directory
# Set this as a cron job and preferably sync the backup directory to cloud / reliable server
TIME=`date +%b-%d-%y`
FILENAME=HA-Config-Backup-$TIME.tar.gz
SRCDIR=$(dirname "$0"})/../config
DESDIR=$(dirname "$0"})/../backups
BACKUPNAME="$DESDIR/$FILENAME"
mkdir -p $DESDIR
tar -cpzf $BACKUPNAME $SRCDIR
echo "Backed up $SRCDIR to $BACKUPNAME"

# Delete backups older than 10 days
find $DESDIR -name 'HA-Config-Backup-*.tar.gz' -mtime +10 -exec rm {}\;
echo "Deleted backups older than 10 days"