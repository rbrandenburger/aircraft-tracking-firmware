import math
import os
import csv
from pathlib import Path

def decode_airborne_velocities(binaryString):

  subType = int(binaryString[5:8], 2)
  intentChangeFlag = binaryString[8]
  IfrCapabilityFlag = binaryString[9]
  nuc = binaryString [10:13] #Navigation Uncertainty Category
  subTypeFields = binaryString[13:35]
  vRateSource = binaryString[35]
  vRateSign = binaryString[36]
  vRate = binaryString[37:46]
  altDifSign = binaryString[48]
  altDif = binaryString[49:56]
  airborneVelocities = {
    'intentChangeFlag' :  intentChangeFlag,
    'IfrCapabilityFlag' : IfrCapabilityFlag,
  }

  #Get the expected error value
  airborneVelocities = airborneVelocities | get_figures_of_merit(nuc)

  #Then get vertical velocity
  airborneVelocities = airborneVelocities | get_vertical_rate(vRateSource, vRateSign, vRate)
  airborneVelocities = airborneVelocities | get_altitude_difference(altDifSign, altDif)
  
  #Then get horizontal velocity. (Could be either ground or air speed)
  if (subType <= 2):
    airborneVelocities = airborneVelocities | get_ground_speed(subType, subTypeFields)
  else:
    airborneVelocities = airborneVelocities | get_air_speed(subType, subTypeFields)

  return airborneVelocities

def get_figures_of_merit(nuc):

  nuc = int(nuc, 2)
  hFOM = vFOM = "NUC value is not defined"
  figuresOfMerit = {'horizontalError' : hFOM, 'verticalError': vFOM} 
  
  if(nuc <= 4):
    currentPath = os.path.dirname(__file__)
    nucTablePath = os.path.join(Path(currentPath).parents[0], ".\\lookup_tables\\navigationUncertainty.csv")
    nucTable = csv.reader(open(nucTablePath, "r"), delimiter=",")
    next(nucTable) #<- Skip table header
    
    for row in nucTable:
      if(int(row[0]) == nuc):
        figuresOfMerit['horizontalError'] = row[1]
        figuresOfMerit['verticalError'] = row[2]
  
  return figuresOfMerit
  

def get_vertical_rate(vRateSource, vRateSign, vRateBinary):
  
  verticleRate = dict()
  vRateDecimal = int(vRateBinary, 2)

  if(vRateSource == '0'):
    verticleRate['vRateSource'] = "GNSS"
  else:
    verticleRate['vRateSource'] = "Barometric"

  if(vRateSign == '0'):
    verticleRate['verticleSpeed'] = 64 * (vRateDecimal + -1)
  else:
    verticleRate['verticleSpeed'] = -( 64 * (vRateDecimal + -1))

  return verticleRate

def get_altitude_difference(altDifSign, altDifBinary):

  altitudeDiff = dict()
  altDifDecimal = int(altDifBinary, 2)
  if(altDifDecimal == 0):
    altitudeDiff['altitudeDifference'] = "No altitude difference information available"
  elif(altDifSign == '0'):
    altitudeDiff['altitudeDifference'] = (altDifDecimal + -1) * 25
  else:
    altitudeDiff['altitudeDifference'] = -(altDifDecimal + -1) * 25

  return altitudeDiff

def get_ground_speed(subType, subTypeFields):

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

  groundSpeed['velocityX'] = speedFactor * speed_function(directionEW, velocityDecimalEW)
  groundSpeed['velocityY'] = speedFactor * speed_function(directionNS, velocityDecimalNS)

  groundSpeed['finalVelocity'] = math.sqrt(groundSpeed['velocityX'] ** 2 + groundSpeed['velocityY'] ** 2)
  groundSpeed['trackAngle'] = math.atan2(groundSpeed['velocityX'], groundSpeed['velocityY']) * (360/(2*math.pi))
  groundSpeed['trackAngle'] %= 360 # <- In case of a negative value

  return groundSpeed

def get_air_speed(subType, subTypeFields):
  
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
    airSpeed['trueAirSpeed'] = speedFactor * speed_function(0, airSpeedDecimal)
  else:
    airSpeed['indicatedAirSpeed'] = speedFactor * speed_function(0, airSpeedDecimal)

  return airSpeed

#Speed formula used for horizontal speed functions
def speed_function(sign, velocity):
  if(velocity == 0):
    return "No information available"
  if(sign):
    return -(velocity - 1)
  else:
    return velocity - 1

  
