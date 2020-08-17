# Vacuum's room from text input

# Room ids for Roborock S5 Max vacuum cleaner
roomIdMap = {
	"hallway": 16,
	"bedroom": 17,
	"bathroom": 18,
	"ensuite": 20,
	"kitchen": 21,
	"guestroom": 22,
	"dining": 23,
	"lounge": 24
}

# Get the room phrase
roomPhrase = data.get("room_phrase").lower()

# A list of roomIds to clean for the vacuum cleaner command 
roomIdsToClean = []

for roomName, roomId in roomIdMap.items():
	if roomName in roomPhrase:
		roomIdsToClean.append(roomId)

# Send command to robot vacuum
service_data = {
	"entity_id": "vacuum.kevin_clean", 
	"command": "app_segment_clean",
	"params": roomIdsToClean
}
hass.services.call(
	"vacuum", 
	"send_command", 
	service_data, 
	False
)
