# Install OS and basics setup
----
1. Get [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)
2. I used 64-bit Ubuntu server 20.04 LTS
3. Enable [SSH access](https://pimylifeup.com/ubuntu-server-raspberry-pi/) before powering up the Pi
4. Change hostname if (optional)
5. Allocate static IP on the router (optional)

# Setup Docker
----
- Install [docker and docker compose using instructions here](https://devdojo.com/bobbyiliev/how-to-install-docker-and-docker-compose-on-raspberry-pi)

# Setup ADB
----
This is required for the Android TV integration.
- Install adb `sudo apt install android-tools-adb`
- Authorize adb with the TV `adb connect TV_IP`
- Clone this repo
- Copy authorized key to config `cp ~/.android/adbkey config/adbkey`

# Setup backups (optional)
----
- Open crontab with `crontab -e`
- Add this cronjob to enable backups `0 2 * * * /bin/sh /home/ubuntu/home-assistant-config/host-scripts/backup-config.sh`
- Also [setup Google drive backups](https://medium.com/@artur.klauser/mounting-google-drive-on-raspberry-pi-f5002c7095c2) while you are at it