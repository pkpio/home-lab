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

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)

  if state.state == 'problem':
    problem = state.attributes.get('problem') or 'none'
    if "conductivity low" in problem:
      send_notification(
        title = state.attributes.get('friendly_name') + " needs 💩💩💩",
        message = "Feed me fertilizer please",
        ledColor = "yellow",
        image = state.attributes.get('entity_picture'),
        tag = state.attributes.get('sensors')['conductivity']
      )
    if "moisture low" in problem:
      send_notification(
        title = state.attributes.get('friendly_name') + " needs 💧💧💧",
        message = "Water me please",
        ledColor = "blue",
        image = state.attributes.get('entity_picture'),
        tag = state.attributes.get('sensors')['moisture']
      )