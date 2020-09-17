# Clears notifications for each plant that needs care

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

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)
  clear_notification(
    tag = plant_state.attributes.get('sensors')['moisture']
  )
