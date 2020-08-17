#!/bin/sh
# Creates an archive of docker-volume each day at rclone/backups
# rclone/backups itself won't be part of this archive

TIME=`date +%b-%d-%y`
ARCHIVE_FILENAME=all-containers-data-$TIME.tar.gz

SOURCE_DIR=/all-containers-data
DESTINATION_DIR=/backups
ARCHIVE_FILEPATH="$DESTINATION_DIR/$ARCHIVE_FILENAME"

tar --exclude='**/rclone/backups*' -cpzf $ARCHIVE_FILEPATH $SOURCE_DIR
echo "Backed up $ARCHIVE_FILEPATH to $SOURCE_DIR"

# Delete backups older than 10 days
find $DESTINATION_DIR -name 'all-containers-data-*.tar.gz' -mtime +10 -exec rm {} \;
echo "Deleted backups older than 10 days"
