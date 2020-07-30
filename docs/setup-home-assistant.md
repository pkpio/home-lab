# Setting up Home assistant
----
This setup is required before we can spin an instance of Home assistant from the config in this repo.

#1 Setup variables for docker containers
----
These are required for different docker services that are part of this Home assistant instance

- Make a copy of each file in `../docker-env/` without the `.sample` extension at the end
- Set the variables in each file

#2 Setup home assistant secrets
----
Now we need to set the secrets required within the Home assistant configuration

- Make a copy of the `../config/secrets.yaml.sample`
- Set each variable in this file
