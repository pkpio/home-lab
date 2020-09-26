# Sends seperate notifications for each plant that needs care
# the notification will include the plant picture 

def send_notification(title, message, ledColor, image, imortance, tag, channel):
  hass.services.call(
    "notify", 
    "notify", 
    {
      "title": title, 
      "message": message,
      "data": {
        "channel": channel,
        "importance": imortance,
        "ledColor": ledColor,
        "clickAction": "/lovelace/plant-monitoring",
        "image": image,
        "tag": tag
      }
    }, 
    False
  )

# State of notifications
water_notifications = hass.states.get("input_boolean.plant_water_notifications").state
fertilize_notifications = hass.states.get("input_boolean.plant_fertilize_notifications").state

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)

  if state.state == 'problem':
    problem = state.attributes.get('problem') or 'none'
    if "conductivity low" in problem and fertilize_notifications == 'on':
      send_notification(
        title = state.attributes.get('friendly_name') + " needs 💩💩💩",
        message = "Fertilizer level at {} {}".format(
                    state.attributes.get('conductivity'), 
                    state.attributes.get('unit_of_measurement_dict')['conductivity']),
        ledColor = "yellow",
        image = state.attributes.get('entity_picture'),
        imortance = "min",
        tag = state.attributes.get('sensors')['conductivity'],
        channel = "Plant fertilizer"
      )
    if "moisture low" in problem and water_notifications == 'on':
      send_notification(
        title = state.attributes.get('friendly_name') + " needs 💧💧💧",
        message = "Water level at {} {}".format(
                    state.attributes.get('moisture'), 
                    state.attributes.get('unit_of_measurement_dict')['moisture']),
        ledColor = "blue",
        image = state.attributes.get('entity_picture'),
        imortance = "low",
        tag = state.attributes.get('sensors')['moisture'],
        channel = "Plant water"
      )