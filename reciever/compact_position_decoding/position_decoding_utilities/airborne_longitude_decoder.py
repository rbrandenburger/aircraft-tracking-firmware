import common_functions as utils
import math

def get_longitude(cprEven, cprOdd, latitude):

  zoneNum = utils.get_longitude_zone_number(latitude)

  lonCprEven = int(cprEven, 2) / (2**17)
  lonCprOdd = int(cprOdd, 2) / (2**17)

  lon_index = get_longitude_index(lonCprEven, lonCprOdd, zoneNum)

  numLonZoneEven = math.max(zoneNum, 1)
  numLonZoneOdd = math.max(zoneNum - 1, 1) #TODO: Check if this is a bug

  lonZoneSizeEven = 360 / numLonZoneEven
  lonZoneSizeOdd = 360 / numLonZoneOdd

  lonEven = lonZoneSizeEven * (utils.modulo_function(lon_index, numLonZoneEven) + lonCprEven)
  lonOdd = lonZoneSizeOdd * (utils.modulo_function(lon_index, numLonZoneOdd) + lonCprOdd)

  #TODO: Implement timestamp decision

  longitude = lonEven

  if(longitude >= 180 ):
    longitude -= 180

  return longitude

def get_longitude_index(lonCprEven, lonCprOdd, zoneNum):
  x = lonCprEven * (zoneNum - 1)
  y = lonCprOdd * zoneNum + 0.5
  lon_index = math.floor(x - y)
  return lon_index
