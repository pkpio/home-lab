#!/bin/sh
# Creates an archive of everything in the repo's local copy.
# Certain paths are included as they are not essential to a 
# restore in the event of a failure or migration. 

TIME=`date +%b-%d-%y`
ARCHIVE_FILENAME=home-lab-$TIME.tar.gz

SOURCE_DIR=/home-lab
DESTINATION_DIR=/backups
ARCHIVE_FILEPATH="$DESTINATION_DIR/$ARCHIVE_FILENAME"

# Bundle everything except excluded data
# - Exclude cloud-backup/backups/ that's where we create backups
# - Exclude /torrent-client/data/incomplete/ where we keep pending downloads
# - Exclude media-server/data/ where we keep downloaded files
# - Exclude media-server/transcode/ where PMS keeps transcoding caches
# - Exclude Plex Media Server/Cache/ where PMS keeps caches
tar \
	--exclude='**/cloud-backup/backups' \
	--exclude='**/transmission/data/downloads' \
        --exclude='**/transmission/data/incomplete' \
        --exclude='**/transmission/data/transmission-home/transmission.log' \
        --exclude='**/radarr/data/logs' \
        --exclude='**/radarr/data/logs.db' \
        --exclude='**/radarr/data/MediaCover' \
        --exclude='**/sonarr/data/logs' \
        --exclude='**/sonarr/data/logs.db' \
        --exclude='**/sonarr/data/MediaCover' \
	--exclude='**/plex-media-server/data' \
	--exclude='**/plex-media-server/transcode' \
	--exclude='**/Plex Media Server/Cache' \
        --exclude='**/Plex Media Server/Logs' \
        --exclude='**/Plex Media Server/Media' \
        --exclude='**/Plex Media Server/Metadata' \
        --exclude='**/Plex Media Server/Plug-in Support/Caches' \
        --exclude='**/.git' \
	-cpzf $ARCHIVE_FILEPATH $SOURCE_DIR
echo "Backed up $SOURCE_DIR to $ARCHIVE_FILEPATH"

# Delete backups older than 1 day(s)
find $DESTINATION_DIR -name 'home-lab-*.tar.gz' -mtime +1 -exec rm {} \;
echo "Deleted backups older than 1 day(s) old"
