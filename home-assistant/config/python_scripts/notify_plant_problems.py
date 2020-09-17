# Sends seperate notifications for each plant that needs care
# the notification will include the plant picture 

waterPlants = []
fertilizePlants = []

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)
  if state.state == 'problem':
    problem = state.attributes.get('problem') or 'none'
    if "conductivity low" in problem:
      fertilizePlants.append(state)
    if "moisture low" in problem:
      waterPlants.append(state)

# Notify about each plant that needs water
for plant_state in waterPlants:
  hass.services.call(
    "notify", 
    "notify", 
    {
      "title": plant_state.attributes.get('friendly_name') + " needs 💧💧", 
      "message": "Water me!",
      "data": {
        "image": plant_state.attributes.get('entity_picture')
      }
    }, 
    False
  )

# Notify about each plant that needs fertilizer
for plant_state in fertilizePlants:
  hass.services.call(
    "notify", 
    "notify", 
    {
      "title": plant_state.attributes.get('friendly_name') + " needs 💩💩", 
      "message": "Feed me!",
      "data": {
        "image": plant_state.attributes.get('entity_picture')
      }
    }, 
    False
  )
