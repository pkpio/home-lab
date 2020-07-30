Home assistant config
----
This repo contains the config and setup instructions for the home assistant instance that runs at my home

Setup
----
We discuss in the order this should be done. I'm using the docker based approach to install Home assistant.

#1 Setup host OS
----
I run my Home Assistant on a Raspberry Pi 4. See [setup instructions](docs/setup-host-os.md).

#2 Setup home-assistant
----
We need to setup some secrets before we can spin up our Home assistant instance for the first time. See [setup instructions](docs/setup-home-assistant.md).

#3 Spin up Home Assistant
----
Just run `docker-compose up -d` to bring up Home Assistant and all other services.

Devices
----
Devices in the home

### Lights
----
- Philips Hue GU10 color spot lights