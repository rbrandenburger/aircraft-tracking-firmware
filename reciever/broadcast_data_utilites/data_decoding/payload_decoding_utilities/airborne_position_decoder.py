def decode_airborne_postition(typeCode, binaryString):
  encodedSurveillanceStatus = binaryString[5:7]
  singleAntennaFlag =  binaryString[7]
  encodedAltitude = binaryString[8:20]
  timeBit = binaryString[20]
  cprFormat = binaryString[21]
  encodedLatitude = binaryString[22:39]
  encodedLongitude = binaryString[39:56]

  surveillanceStatus = get_surveillance_status(encodedSurveillanceStatus)
  altitude = decode_altitude(typeCode, encodedAltitude)

  airbornePosition = {
    'surveillanceStatus' : surveillanceStatus,
    'singleAntennaFlag' : singleAntennaFlag,
    'altitude' : altitude,
    'timeBit' : timeBit,
    'cprFormat' : cprFormat,
    'encodedLatitude' : encodedLatitude,
    'encodedLongitude' : encodedLongitude
  }

  return airbornePosition

def decode_altitude(typeCode, encodedAltitude):
  #Check for all 0 bits
  if(int(encodedAltitude, 2) == 0):
    return "No altitude information available"

  if(typeCode <= 18):
    altitude = decode_barometric_altitude(encodedAltitude)
  else:
    altitude = decode_gnss_altitude(encodedAltitude)

  return altitude

def decode_barometric_altitude(encodedAltitude):
  qBit = encodedAltitude[7]
  encodedAltitude = encodedAltitude[:7] + encodedAltitude[8:]

  if(qBit):
    altitude = int(encodedAltitude, 2)
    altitude = 25 * altitude - 1000
  else:
    #If Q=0, then altitude bits need to be decoded from gray code into binary.
    altitude = int(decode_gray_to_binary(encodedAltitude), 2)
    altitude = 100 * altitude

  return str(altitude) + " ft"

def decode_gnss_altitude(encodedAltitude):
  altitude = int(encodedAltitude, 2)
  return str(altitude) + " m"

def decode_gray_to_binary(gray):
  binary = gray[0]
  gray = gray[1:]

  while (len(gray) > 0):
    if(gray[0] == binary[-1]):
      binary = binary + '0'
    else:
      binary = binary + '1'

    gray = gray[1:]

  return binary

def get_surveillance_status(encodedSurveillanceStatus):
  match encodedSurveillanceStatus:
    case '00':
      surveillanceStatus = "No Condition"
    case '01':
      surveillanceStatus = "Permanent Alert"
    case '10':
      surveillanceStatus = "Temporary Alert"
    case '11':
      surveillanceStatus = "SPI Condition"
    case _:
      surveillanceStatus = "Invalid surveillance status"
  
  return surveillanceStatus