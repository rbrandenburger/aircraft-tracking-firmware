import os
import csv
from pathlib import Path

def decode_aircraft_identification(typeCode, binaryString):
  #This has two parts: Wake Vortex and Callsign
  currentPath = os.path.dirname(__file__)
  wakeVortex = get_wake_vortex(typeCode, binaryString, currentPath)
  callsign = get_callsign(binaryString, currentPath)
  return {'wakeVortex' : wakeVortex, 'callsign': callsign}

def get_wake_vortex(typeCode, binaryString, currentPath):
  #Wake vortex is determined by two values: typeCode and category
  wakeVortex = "Undefined"
  category = int(binaryString[5:8], 2)

  if(typeCode == 1):
    wakeVortex = "Reserved"
  elif(category == 0):
    pass
  else:
    #Load table that has typeCode and Category combos
    wakeTablePath = os.path.join(Path(currentPath).parents[0], ".\\lookup_tables\\wakeVortexEncoding.csv")
    wakeTable = csv.reader(open(wakeTablePath, "r"), delimiter=",")

    for row in wakeTable:
      if(int(row[0]) == typeCode and int(row[1]) == category):
        wakeVortex = row[2]
  
  return wakeVortex

def get_callsign(binaryString, currentPath):
  binaryString = binaryString[8:]
  if(len(binaryString) != 48):
    return "Error: Message too short; does not follow ADSB standards"
  else:
    callsign = ""

    #Need to load charTable into memory, as a reader will not reset for the nested loop
    charTablePath = os.path.join(Path(currentPath).parents[0], ".\\lookup_tables\\adsbCharEncoding.csv")
    charTableReader = csv.reader(open(charTablePath, "r"), delimiter=",")
    charTableList = list(charTableReader)

    #Characters are encoded using ASCII but minus two leading bits in the standard 8-bit encoding
    while (len(binaryString) > 0):
      encodedChar = binaryString[:6]

      for row in charTableList:
        if(encodedChar == row[0]):
          callsign += row[1]
          break

      binaryString = binaryString[6:]

    return callsign