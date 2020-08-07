#!/bin/sh
# Creates an archive of docker-volume each day at docker-volume/rclone/data
# docker-volume/rclone/data itself won't be part of this archive

TIME=`date +%b-%d-%y`
ARCHIVE_FILENAME=docker-volume-$TIME.tar.gz

SOURCE_DIR=/docker-volume
DESTINATION_DIR=/docker-volume/rclone/data
ARCHIVE_FILEPATH="$DESTINATION_DIR/$ARCHIVE_FILENAME"

tar --exclude='**/rclone/data/*' -cpzf $ARCHIVE_FILEPATH $SOURCE_DIR
echo "Backed up $ARCHIVE_FILEPATH to $SOURCE_DIR"

# Delete backups older than 10 days
find $DESTINATION_DIR -name 'docker-volume-*.tar.gz' -mtime +10 -exec rm {} \;
echo "Deleted backups older than 10 days"
