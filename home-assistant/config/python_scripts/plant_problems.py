#
# DIYFUTURISM.COM
# PLANT_PROBLEMS.PY
# Make a list of all plants that need to be water and fertilized and combine into readable lists.
#
# Creates:
# sensor.plants_water_low
# sensor.plants_fertilizer_low
# sensor.plants_battery_low
# sensor.plants_problems
#
#  http://www.diyfuturism.com/making-houseplants-talk

allproblemPlants = []
waterPlants = []
fertilizePlants = []
lowBatteryPlants = []
whichIcon = "mdi:help-circle-outline"

for entity_id in hass.states.entity_ids('plant'):
  state = hass.states.get(entity_id)
  if state.state == 'problem':
    problem = state.attributes.get('problem') or 'none'
    if "conductivity low" in problem:
      fertilizePlants.append(state.name)
    if "moisture low" in problem:
      waterPlants.append(state.name)
    if "battery low" in problem:
      lowBatteryPlants.append(state.name)

# Make a list of all problems
allproblemPlants.extend(fertilizePlants)
allproblemPlants.extend(waterPlants)
allproblemPlants.extend(lowBatteryPlants)
allproblemPlants = set(allproblemPlants)

# Set icon
if allproblemPlants:
  whichIcon = "mdi:alert-circle-outline"
else:
  whichIcon = "mdi:check-circle-outline"

# Set states
hass.states.set('sensor.plants_problems', len(allproblemPlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Problem Plants',
    'icon': whichIcon,
    'problem_plants': allproblemPlants,
    'water': waterPlants,
    'water_number': len(waterPlants),
    'fertilize': fertilizePlants,
    'fertilize_number': len(fertilizePlants),
    'battery_low': lowBatteryPlants,
    'battery_low_number': len(lowBatteryPlants)
})

hass.states.set('sensor.plants_water_low', len(waterPlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Water plants count',
    'icon': 'mdi:water',
    'plants': waterPlants
})

hass.states.set('sensor.plants_fertilizer_low', len(fertilizePlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Fertilize plants count',
    'icon': 'mdi:emoticon-poop',
    'plants': fertilizePlants
})

hass.states.set('sensor.plants_battery_low', len(fertilizePlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Battery low plants',
    'icon': 'mdi:battery-alert',
    'plants': lowBatteryPlants
})

