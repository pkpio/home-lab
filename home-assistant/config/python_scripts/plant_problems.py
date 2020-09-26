#
# DIYFUTURISM.COM
# PLANT_PROBLEMS.PY
# Make a list of all plants that need to be water and fertilized and combine into readable lists.
#
# Creates:
# sensor.plants_total
# sensor.plants_problem
# sensor.plants_water_low
# sensor.plants_fertilizer_low
# sensor.plants_battery_low
#
#  http://www.diyfuturism.com/making-houseplants-talk

allproblemPlants = []
waterPlants = []
fertilizePlants = []
lowBatteryPlants = []
whichIcon = "mdi:help-circle-outline"

plant_entities = hass.states.entity_ids('plant')

for entity_id in plant_entities:
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
hass.states.set('sensor.plants_total', len(plant_entities), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Total Plants',
    'icon': 'mdi:leaf'
})

hass.states.set('sensor.plants_problem', len(allproblemPlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Plants with issues',
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
    'friendly_name': 'Plants that need water',
    'icon': 'mdi:water',
    'plants': waterPlants
})

hass.states.set('sensor.plants_fertilizer_low', len(fertilizePlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Plants that need fertilizer',
    'icon': 'mdi:emoticon-poop',
    'plants': fertilizePlants
})

hass.states.set('sensor.plants_battery_low', len(fertilizePlants), {
    'unit_of_measurement': 'plants',
    'friendly_name': 'Plant sensors with low Battery',
    'icon': 'mdi:battery-alert',
    'plants': lowBatteryPlants
})

