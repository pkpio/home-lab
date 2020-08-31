#!/bin/sh
# Creates an archive of everything in the repo's local copy.
# Certain paths are included as they are not essential to a 
# restore in the event of a failure or migration. 

TIME=`date +%b-%d-%y`
ARCHIVE_FILENAME=all-containers-data-$TIME.tar.gz

SOURCE_DIR=/all-containers-data
DESTINATION_DIR=/backups
ARCHIVE_FILEPATH="$DESTINATION_DIR/$ARCHIVE_FILENAME"

# Bundle everything except excluded data
# - Exclude cloud-backup/backups/ that's where we create backups
# - Exclude /torrent-client/data/incomplete/ where we keep pending downloads
# - Exclude media-server/data/ where we keep downloaded files
# - Exclude media-server/transcode/ where PMS keeps transcoding caches
# - Exclude Plex Media Server/Cache/ where PMS keeps caches
tar \
	--exclude='**/cloud-backup/backups/*' \
	--exclude='**/torrent-client/data/incomplete/*' \
	--exclude='**/media-server/data/*' \
	--exclude='**/media-server/transcode/*' \
	--exclude='**/Plex Media Server/Cache/*'
	-cpzf $ARCHIVE_FILEPATH $SOURCE_DIR
echo "Backed up $SOURCE_DIR to $ARCHIVE_FILEPATH"

# Delete backups older than 10 days
find $DESTINATION_DIR -name 'all-containers-data-*.tar.gz' -mtime +10 -exec rm {} \;
echo "Deleted backups older than 10 days"
