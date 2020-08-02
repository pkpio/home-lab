# Updates the initial brightness value of the lights based on time of the day
brightnessPoints = {
	"00:30": 120,
	"08:00": 150,
	"17:00": 180,
	"19:00": 220,
	"22:30": 255,
	"23:30": 150
}

# Based on minute of the day
minutePoints = []
for timePoint, brightness in brightnessPoints.items():
	hours, minutes = timePoint.split(':')
	minuteOfDay = int(hours) * 60 + int(minutes)
	minutePoints.append({
		"minuteOfDay": minuteOfDay,
		"brightness": brightness
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
nowBrightness = int(sortedPoints[leftIndex]['brightness'] * leftWeight + sortedPoints[rightIndex]['brightness'] * rightWeight)

# Set the brightness input value on HA
service_data = {
	"entity_id": "input_number.contextual_brightness", 
	"value": nowBrightness
}
hass.services.call(
	"input_number", 
	"set_value", 
	service_data, 
	False
)
