# Install OS and basics setup
----
- I run on Ubuntu 20.04 server
- Allocate static IP on the router (optional)

# Docker & docker-compose
----
- Install Docker 
- Install docker-compose
- Change the images in docker-compose to match your system arch type

# ADB authentication for Home Assistant
----
This is required for the Android TV integration.
- Install adb `sudo apt install android-tools-adb`
- Authorize adb with the TV `adb connect TV_IP`
- Copy authorized key to config `cp ~/.android/adbkey home-assistant/config/adbkey`

# Cloud sync for backups
----
- Authorize a cloud service with cloud-backup container. It runs rsync - check docs for how to authenticate a service. Name the service as `cloud` to avoid having to make changes in `docker-compose.yaml`

# Plex Media Server
----
Check [docs here](https://github.com/plexinc/pms-docker)
- Needs Plex claim code unless you are migrating an existing instance

# Deconz
----
Check [docs here](https://phoscon.de/en/conbee/install#docker)
- Grant USB permissions to current user `sudo usermod -a -G dialout $USER`
- Check that deconz USB stick is mounted at `/dev/ttyACM0` if not
	- Change device in `docker-compose.yml`
	- Change device in `zigbee-app/.env`
