# Updates the initial brightness value of the lights based on time of the day
# Color temp between 153 to 500 (blue to yellow light)
brightnessPoints = {
	"00:30": {
		"startBrightness": 100,
		"finalBrightness": 150,
		"transitionTime": 45,
		"colorTemperature": 400
	},
	"08:00": {
		"startBrightness": 140,
		"finalBrightness": 200,
		"transitionTime": 15,
		"colorTemperature": 300
	},
	"17:00": {
		"startBrightness": 170,
		"finalBrightness": 220,
		"transitionTime": 10,
		"colorTemperature": 200
	},
	"19:00": {
		"startBrightness": 190,
		"finalBrightness": 230,
		"transitionTime": 10,
		"colorTemperature": 153
	},
	"22:30": {
		"startBrightness": 210,
		"finalBrightness": 255,
		"transitionTime": 15,
		"colorTemperature": 200
	},
	"23:30": {
		"startBrightness": 160,
		"finalBrightness": 200,
		"transitionTime": 20,
		"colorTemperature": 300
	}
}

# Based on minute of the day
minutePoints = []
for timePoint, contextData in brightnessPoints.items():
	hours, minutes = timePoint.split(':')
	minuteOfDay = int(hours) * 60 + int(minutes)
	minutePoints.append({
		"minuteOfDay": minuteOfDay,
		"contextData": contextData
	})
sortedPoints = sorted(minutePoints, key = lambda point: point['minuteOfDay'])

# Find the minute of day right now
nowHour = int(data.get("hour"))
nowMinute = int(data.get("minute"))
minuteOfDay = nowHour * 60 + nowMinute

leftIndex, rightIndex = -1, -1

# Find leftIndex in the loop
for index in range(len(sortedPoints)):
	if sortedPoints[index]['minuteOfDay'] >= minuteOfDay:
		rightIndex = index
		break

# If point found
rightIndex = 0 if rightIndex == -1 else rightIndex
leftIndex = rightIndex - 1 if rightIndex != 0 else len(sortedPoints) - 1

leftRatio, rightRatio = 0.0, 0.0

if sortedPoints[rightIndex]['minuteOfDay'] > sortedPoints[leftIndex]['minuteOfDay']:
	# both points fall on the same day - simple scenario
	pointDistance = sortedPoints[rightIndex]['minuteOfDay'] - sortedPoints[leftIndex]['minuteOfDay']
	leftRatio = (minuteOfDay - sortedPoints[leftIndex]['minuteOfDay']) / pointDistance
	rightRatio = 1.0 - leftRatio
else:
	# points are on either side of the day
	pointDistance = 1440 - sortedPoints[leftIndex]['minuteOfDay'] + sortedPoints[rightIndex]['minuteOfDay']
	if minuteOfDay <= sortedPoints[rightIndex]['minuteOfDay']:
		# current time is in the day of right point
		rightRatio = (sortedPoints[rightIndex]['minuteOfDay'] - minuteOfDay) / pointDistance
		leftRatio = 1.0 - rightRatio
	else:
		# current time is in the day of left point
		leftRatio = (minuteOfDay - sortedPoints[leftIndex]['minuteOfDay']) / pointDistance
		rightRatio = 1.0 - leftRatio

leftWeight, rightWeight = (1 - leftRatio), (1 - rightRatio)

weightedIntVal = lambda key : int(sortedPoints[leftIndex]['contextData'][key] * leftWeight + sortedPoints[rightIndex]['contextData'][key] * rightWeight)


#### Set the start brightness ####
hass.services.call(
	"input_number", 
	"set_value", 
	{
		"entity_id": "input_number.contextual_start_brightness", 
		"value": weightedIntVal('startBrightness')
	}, 
	False
)

#### Set the final brightness ####
hass.services.call(
	"input_number", 
	"set_value", 
	{
		"entity_id": "input_number.contextual_final_brightness", 
		"value": weightedIntVal('finalBrightness')
	}, 
	False
)
#### Set the transition time ####
hass.services.call(
	"input_number", 
	"set_value", 
	{
		"entity_id": "input_number.contextual_transition_time", 
		"value": weightedIntVal('transitionTime')
	}, 
	False
)


#### Set the color temperature ####
hass.services.call(
	"input_number", 
	"set_value", 
	{
		"entity_id": "input_number.contextual_color_temperature", 
		"value": weightedIntVal('colorTemperature')
	}, 
	False
)

