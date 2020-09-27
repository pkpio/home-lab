# Home Lab
----
This repo contains the config for all the services that run on the HomeLab. Here's the list of services that run in their own docker containers:

- **home-assistant** - Runs the open source home automation tool, [Home Assistant](https://www.home-assistant.io/). All the other services are integrated into this in some form.
- **database** - [MariaDB database]((https://mariadb.org/) ) service used by home-assistant
- **zigbee-app** - interacts with [Conbee II](https://phoscon.de/en/conbee2) stick, a universal
Zigbee USB gateway.
- **mqtt-broker** - runs an [Eclipse Mosquitto](https://mosquitto.org/) MQTT broker. There are multiple Raspberry Pi's around the house that gather and report Plant sensor data to the broker. Home assistant consumes this data
- **media-server** - runs a [Plex Media Server](https://www.plex.tv/en-gb/media-server-downloads/). This gives access to the Media hosted on this server to multiple devices in the house
- **monitoring** - runs [Glances](https://nicolargo.github.io/glances/) service to monitor the resources of the Home Lab server.
- **cloud-backup** - uses [rclone](https://rclone.org/) to do daily backups of the HomeLab setup to a cloud service. If something really bad happens, we can always start fresh from the last backup in no time.
- **local-sync** - uses [rsync](https://linux.die.net/man/1/rsync) to periodically move data from Internal to External HD.
- **cron-service** - runs a docker cron service using [Ofelia](https://github.com/mcuadros/ofelia). This allows us to schedule tasks on different containers - used for periodic syncs.
- **torrent-client** - runs a [Transmission](https://transmissionbt.com/) client that's accessible to other devices in the local network.

# Requirements
----
## Hardware
- This instance runs on an [Intel NUC](https://www.intel.co.uk/content/www/uk/en/products/boards-kits/nuc.html). If you want use a [Raspberry Pi](https://www.raspberrypi.org/), you will need to update the `docker-compose.yml` with images suitable for ARM CPU architecture.
- Plugin a [Conbee II](https://phoscon.de/en/conbee2) USB stick plugged into the server

## Software
- Ubuntu (20.04 or any version compatible with your hardware)
- docker 
- docker-compose

For convinence, you may use this [setup-docker.sh](https://github.com/praveendath92/plant-monitor/blob/master/setup-docker.sh) script.


# Setup
----
Most services require some environments variables. Go to each folder and a copy of `.env.sample` to `.env` and fill in the values.

## Home Assistant

### Secrets
- Make a copy of the `home-assistant/config/secrets.yaml.sample` to `home-assistant/config/secrets.yaml`
- Set each variable in this file

### Android TV integration
This is required for the Android TV integration.
- Install adb `sudo apt install android-tools-adb`
- Authorize adb with the TV `adb connect TV_IP`
- Copy authorized key to config `cp ~/.android/adbkey home-assistant/config/adbkey`

## Rsync Cloud backups
- Authorize a cloud service with cloud-backup container. It runs rsync - check docs for how to authenticate a service. Name the service as `cloud` to avoid having to make changes in `docker-compose.yaml`

## Plex Media Server
Check [docs here](https://github.com/plexinc/pms-docker)
- Needs Plex claim code unless you are migrating an existing instance

## deConz Zigbee app
Check [docs here](https://phoscon.de/en/conbee/install#docker)
- Grant USB permissions to current user `sudo usermod -a -G dialout $USER`
- Check that deconz USB stick is mounted at `/dev/ttyACM0` if not
	- Change device in `docker-compose.yml`
	- Change device in `zigbee-app/.env`


# Starting up
----
Just run `docker-compose up -d` to bring up Home Assistant and all other services.
