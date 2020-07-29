Home assistant config
----
This repo contains the config and setup instructions for the home assistant instance that runs at my home

Setup
----
We discuss in the order this should be done. I'm using the docker based approach to install Home assistant.

#1 Setup host OS
----
I run my Home Assistant on a Raspberry Pi 4. See [setup instructions](docs/setup-host-os.md).

#2 Run home-assistant
----
- Clone this repo
- Run `docker-compose up -d`

Devices
----
Devices in the home

### Lights
----
- Philips Hue GU10 color spot lights