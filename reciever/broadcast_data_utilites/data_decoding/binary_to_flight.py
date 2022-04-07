from .. import flight

def GetFlightFromBinary(binaryString):

  downlinkFormat = binaryString[:5]

  if( (int(downlinkFormat, 2)) != 17 ):
    return -1
  else:
    print (downlinkFormat)
    return 1