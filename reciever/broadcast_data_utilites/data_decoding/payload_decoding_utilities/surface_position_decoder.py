import os
import csv
from pathlib import Path

def decode_surface_postion(binaryString):

  encodedMovement = binaryString[5:12]
  trackStatus = binaryString[12]
  track = binaryString[13:20]
  time = binaryString[20]
  cprFormat = binaryString[21]
  encodedLatitude = binaryString[22:39]
  encodedLongitude = binaryString[39:56]

  movement = decode_movment(encodedMovement)
  
  return {'foo' : 'bar'}


def decode_movment(encodedMovement):

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
      "speed" : ">175kt"
    }
  elif(decimalMovement == 0):
    decodedMovement = {
      "state" : "unavailable",
      "speed" : "-1"
      }
  else:
    decodedMovement = calculate_speed()
  
  return decodedMovement

def calculate_speed(decimalMovement):

  currentPath = os.path.dirname(__file__)
  groundSpeedEncodingPath = os.path.join(Path(currentPath).parents[0], ".\\lookup_tables\\groundSpeedEncoding.csv")
  groundSpeedEncodingTable = csv.reader(open(groundSpeedEncodingPath, "r"), delimiter=",")
  next(groundSpeedEncodingTable) #<- Skips the table header

  groundSpeed = {
    "state" : "error",
    "speed" : "-1"
  }

  for row in groundSpeedEncodingTable:
    if (decimalMovement < int(row[0])):
      speed = int(row[3]) + (decimalMovement - row[1]) * row[4]
      groundSpeed = {
        "state" : row[2],
        "speed" : str(speed)
      }

  return groundSpeed
