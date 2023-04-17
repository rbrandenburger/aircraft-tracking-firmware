from utilites.general import table_loader

def decode_surface_postion(binaryString):
  encodedMovement = binaryString[5:12]
  trackStatus = binaryString[12]
  track = binaryString[13:20]
  time = binaryString[20]
  cprFormat = binaryString[21]
  encodedLatitude = binaryString[22:39]
  encodedLongitude = binaryString[39:56]

  movement = _decode_movment(encodedMovement)
  trackAngle = _decode_track_angle(trackStatus, track)
  
  surfacePosition = {
    "movement" : movement,
    "trackAngle" : trackAngle,
    "timeBit" : time,
    "cprFormat" : cprFormat,
    "encodedLatitude" : encodedLatitude,
    "encodedLongitude" : encodedLongitude
  }

  return surfacePosition

# Private methods

def _decode_movment(encodedMovement):
  decodedMovement = ""
  decimalMovement = int(encodedMovement, 2)

  if(decimalMovement == 127):
    decodedMovement = {
      "state" : "reserved",
      "speed" : "-1"
    }
  elif(decimalMovement >= 124):
    decodedMovement = {
      "state" : "Moving",
      "speed" : ">175"
    }
  elif(decimalMovement == 0):
    decodedMovement = {
      "state" : "unavailable",
      "speed" : "-1"
      }
  else:
    decodedMovement = _calculate_speed(decimalMovement)
  
  return decodedMovement

def _calculate_speed(decimalMovement):
  groundSpeedEncodingTable = table_loader.get_table("groundSpeedEncoding.csv")
  groundSpeedEncodingTable.pop(0) #<- removes the table header

  groundSpeed = {
    "state" : "error",
    "speed" : "-1"
  }

  for row in groundSpeedEncodingTable:
    if (decimalMovement < int(row[0])):
      speed = int(row[3]) + (decimalMovement - int(row[1])) * int(row[4])
      groundSpeed = {
        "state" : row[2],
        "speed" : str(speed)
      }
      return groundSpeed

  return groundSpeed

def _decode_track_angle(trackStatus, track):
  if(int(trackStatus)):
    decimalTrack = int(track, 2)
    trackAngle = str(round((360 * decimalTrack) / 128, 1))
  else:
    trackAngle = "invalid"

  return trackAngle
