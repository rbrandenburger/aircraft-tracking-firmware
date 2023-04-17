import math
from utilites.general import table_loader

def decode_airborne_velocities(binaryString):
  subType = int(binaryString[5:8], 2)
  intentChangeFlag = binaryString[8]
  IfrCapabilityFlag = binaryString[9]
  nuc = binaryString [10:13] #Navigation Uncertainty Category
  subTypeFields = binaryString[13:35]
  verticalVelocitySource = binaryString[35]
  verticalVelocitySign = binaryString[36]
  encodedVerticalVelocity = binaryString[37:46]
  altDifSign = binaryString[48]
  encodedAltDif = binaryString[49:56]
  
  figuresOfMerit = _decode_figures_of_merit(nuc)
  verticalVelocity = _decode_vertical_velocity(verticalVelocitySign, encodedVerticalVelocity)
  altDif = _decode_altitude_difference(altDifSign, encodedAltDif)
  
  if(int(verticalVelocitySource)):
    verticalVelocitySource = "Barometric"
  else:
    verticalVelocitySource = "GNSS"

  if (subType <= 2):
    horizontalVelocity = _decode_ground_speed(subType, subTypeFields)
  else:
    horizontalVelocity = _decode_air_speed(subType, subTypeFields)

  airborneVelocities = {
    'intentChangeFlag' :  intentChangeFlag,
    'IfrCapabilityFlag' : IfrCapabilityFlag,
    'figuresOfMerit' : figuresOfMerit,
    'verticalVelocitySource' : verticalVelocitySource,
    'verticalVelocity' : verticalVelocity,
    'altDif' : altDif,
    'horizontalVelocity' : horizontalVelocity
  }

  return airborneVelocities

# Private methods

def _decode_figures_of_merit(nuc):
  nuc = int(nuc, 2)
  hFOM = vFOM = "NUC value is not defined"
  figuresOfMerit = {'horizontalError' : hFOM, 'verticalError': vFOM} 
  
  if(nuc <= 4):
    nucTable = table_loader.get_table("navigationUncertainty.csv")
    nucTable.pop(0) #<- Removes table header
    
    for row in nucTable:
      if(int(row[0]) == nuc):
        figuresOfMerit['horizontalError'] = row[1]
        figuresOfMerit['verticalError'] = row[2]
  
  return figuresOfMerit
  

def _decode_vertical_velocity(verticalRateSign, encodedVerticalRate):
  verticalRateDecimal = int(encodedVerticalRate, 2)

  if(verticalRateSign == '0'):
    verticleVelocity = 64 * (verticalRateDecimal + -1)
  else:
    verticleVelocity = -( 64 * (verticalRateDecimal + -1))

  return verticleVelocity

def _decode_altitude_difference(altDifSign, altDifBinary):
  altDifDecimal = int(altDifBinary, 2)
  if(altDifDecimal == 0):
    altDif = "No altitude difference information available"
  elif(altDifSign == '0'):
    altDif = str((altDifDecimal + -1) * 25)
  else:
    altDif = str(-(altDifDecimal + -1) * 25)

  return altDif

def _decode_ground_speed(subType, subTypeFields):
  groundSpeed = dict()
  directionEW = subTypeFields[0]
  velocityBinaryEW = subTypeFields[1:11]
  velocityDecimalEW = int(velocityBinaryEW, 2)
  directionNS = subTypeFields[11]
  velocityBinaryNS = subTypeFields[12:22]
  velocityDecimalNS = int(velocityBinaryNS, 2)
  speedFactor = 1
  if(subType == 2):
    speedFactor = 4

  velocityX = speedFactor * _speed_function(directionEW, velocityDecimalEW)
  velocityY = speedFactor * _speed_function(directionNS, velocityDecimalNS)

  groundSpeed['speed'] = round(math.sqrt(velocityX ** 2 + velocityY** 2), 1)
  groundSpeed['trackAngle'] = round(math.atan2(velocityX, velocityY) * (360/(2*math.pi)), 1)
  groundSpeed['trackAngle'] %= 360 # <- In case of a negative value

  return groundSpeed

def _decode_air_speed(subType, subTypeFields):
  airSpeed = dict()
  magneticHeadingStatus = subTypeFields[0]
  magneticHeadingBinary = subTypeFields[1:11]
  magneticHeadingDecimal = int(magneticHeadingBinary, 2)
  airSpeedType = subTypeFields[11]
  airSpeedBinary = subTypeFields[12:22]
  airSpeedDecimal = int(airSpeedBinary, 2)
  speedFactor = 1
  if(subType == 4):
    speedFactor = 4

  if(magneticHeadingStatus):
    airSpeed['magneticHeading'] = magneticHeadingDecimal * (360/1024)
  else:
    airSpeed['magneticHeading'] = "Magnetic heading not available"

  if(airSpeedType):
    airSpeed['trueAirSpeed'] = speedFactor * _speed_function(0, airSpeedDecimal)
  else:
    airSpeed['indicatedAirSpeed'] = speedFactor * _speed_function(0, airSpeedDecimal)

  return airSpeed

#Speed formula used for horizontal speed functions
def _speed_function(sign, velocity):
  if(velocity == 0):
    return "No information available"
  if(int(sign)):
    return -(velocity - 1)
  else:
    return velocity - 1
