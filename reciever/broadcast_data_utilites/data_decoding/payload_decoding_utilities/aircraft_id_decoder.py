from ... import table_loader

def decode_aircraft_identification(typeCode, binaryString):
  category = binaryString[5:8]
  encodedCallsign = binaryString[8:]
  
  wakeVortex = decode_wake_vortex(typeCode, category)
  callsign = decode_callsign(encodedCallsign)

  aircraftID = {
    'wakeVortex' : wakeVortex, 
    'callsign': callsign
    }

  return aircraftID

def decode_wake_vortex(typeCode, category):
  #Wake vortex is determined by two values: typeCode and category
  wakeVortex = "Undefined"
  if(typeCode == 1):
    wakeVortex = "Reserved"
  elif(category == 0):
    pass
  else:
    #Load table that has typeCode and Category combos
    wakeTable = table_loader.get_table("wakeVortexEncoding.csv")
    for row in wakeTable:
      if(int(row[0]) == typeCode and int(row[1]) == category):
        wakeVortex = row[2]
  
  return wakeVortex

def decode_callsign(encodedCallsign):
  if(len(encodedCallsign) != 48):
    return "Error: Message too short; does not follow ADSB standards"
  else:
    callsign = ""
    charTable = table_loader.get_table("adsbCharEncoding.csv")

    #Characters are encoded using ASCII but minus two leading bits in the standard 8-bit encoding
    while (len(encodedCallsign) > 0):
      encodedChar = encodedCallsign[:6]
      for row in charTable:
        if(encodedChar == row[0]):
          callsign += row[1]
          break

      encodedCallsign = encodedCallsign[6:]

    return callsign