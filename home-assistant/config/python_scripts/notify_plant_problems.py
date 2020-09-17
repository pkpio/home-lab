# Sends seperate notifications for each plant that needs care
# the notification will include the plant picture 

def send_notification(title, message, ledColor, image, tag):
  hass.services.call(
    "notify", 
    "notify", 
    {
      "title": title, 
      "message": message,
      "data": {
        "channel": "Plant",
        "importance": "low",
        "ledColor": ledColor,
        "clickAction": "/lovelace/plant-monitoring",
        "image": image,
        "tag": tag
      }
    }, 
    False
  )

def clear_notification(tag):
  hass.services.call(
    "notify", 
    "notify", 
    {
      "message": "clear_notification",
      "data": {
        "tag": tag
      }
    }, 
    False
  )


allPlants = []
waterPlants = []
fertilizePlants = []

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)
  allPlants.append(state)

  if state.state == 'problem':
    problem = state.attributes.get('problem') or 'none'
    if "conductivity low" in problem:
      fertilizePlants.append(state)
    if "moisture low" in problem:
      waterPlants.append(state)

# Clear all existing notifications
for plant_state in allPlants:
  clear_notification(tag = plant_state.attributes.get('sensors')['moisture'])
  clear_notification(tag = plant_state.attributes.get('sensors')['conductivity'])

# Notify about each plant that needs water
for plant_state in waterPlants:
  send_notification(
    title = plant_state.attributes.get('friendly_name') + " needs 💧💧💧",
    message = "Water me please",
    ledColor = "blue",
    image = plant_state.attributes.get('entity_picture'),
    tag = plant_state.attributes.get('sensors')['moisture']
  )

# Notify about each plant that needs fertilizer
for plant_state in fertilizePlants:
  send_notification(
    title = plant_state.attributes.get('friendly_name') + " needs 💩💩💩",
    message = "Feed me fertilizer please",
    ledColor = "yellow",
    image = plant_state.attributes.get('entity_picture'),
    tag = plant_state.attributes.get('sensors')['conductivity']
  )
