# Updates the color value of the lights based on time of the day

colorPoints = {
	"00:30": [255, 255, 255],
	"08:00": [255, 255, 255],
	"17:00": [255, 255, 255],
	"19:00": [255, 255, 255],
	"22:30": [255, 255, 255],
	"23:30": [255, 255, 255]
}

# Based on minute of the day
minutePoints = []
for timePoint, color in colorPoints.items():
	hours, minutes = timePoint.split(':')
	minuteOfDay = int(hours) * 60 + int(minutes)
	minutePoints.append({
		"minuteOfDay": minuteOfDay,
		"color": color
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
nowRed = int(sortedPoints[leftIndex]['color'][0] * leftWeight + sortedPoints[rightIndex]['color'][0] * rightWeight)
nowGreen = int(sortedPoints[leftIndex]['color'][1] * leftWeight + sortedPoints[rightIndex]['color'][1] * rightWeight)
nowBlue = int(sortedPoints[leftIndex]['color'][2] * leftWeight + sortedPoints[rightIndex]['color'][2] * rightWeight)

# Set the red color input value on HA
service_data = {
	"entity_id": "input_number.contextual_color_red", 
	"value": nowRed
}
hass.services.call(
	"input_number", 
	"set_value", 
	service_data, 
	False
)

# Set the green color input value on HA
service_data = {
	"entity_id": "input_number.contextual_color_green", 
	"value": nowGreen
}
hass.services.call(
	"input_number", 
	"set_value", 
	service_data, 
	False
)

# Set the blue color input value on HA
service_data = {
	"entity_id": "input_number.contextual_color_blue", 
	"value": nowBlue
}
hass.services.call(
	"input_number", 
	"set_value", 
	service_data, 
	False
)
