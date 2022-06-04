import os
import csv
from pathlib import Path

def decode_aircraft_identification(typeCode, binaryString):
  #This has two parts: Wake Vortex and Callsign
  #TODO: Split into two functions for easier reading
  #Part 1 - Getting the Wake Vortex
  currentPath = os.path.dirname(__file__)
  wakeVortex = "Undefined"
  category = int(binaryString[5:8], 2)

  #Wake vortex is determined by two values: typeCode and category
  if(typeCode == 1):
    wakeVortex = "Reserved"
  elif(category == 0):
    pass
  else:
    #Load table that has typeCode and Category combos
    wakeTablePath = os.path.join(currentPath, ".\\tables\\wakeVortexEncoding.csv")
    wakeTable = csv.reader(open(wakeTablePath, "r"), delimiter=",")

    for row in wakeTable:
      if(row[0] == typeCode and row[1] == category):
        wakeVortex = row[3]
    
    
  #Part 2 - Getting the callsign
  binaryString = binaryString[8:]

  if(len(binaryString) != 48):
    return "Error: Message too short; does not follow ADSB standards"
  else:
    callsign = ""

    #Need to load charTable into memory, as a reader will not reset for the nested loop
    charTablePath = os.path.join(Path(currentPath).parents[0], ".\\tables\\adsbCharEncoding.csv")
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
  
  return "Message Type: Aircraft Identification\n  -Wake Vortex: {}\n  -Callsign: {}".format(wakeVortex, callsign)