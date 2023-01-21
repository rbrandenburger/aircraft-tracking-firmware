from . import common_functions as utils
import math

def decode_longitude(cprEven, cprOdd, latitude):
  zoneNum = utils.get_longitude_zone_number(latitude)

  lonCprEven = int(cprEven, 2) / (2**17)
  lonCprOdd = int(cprOdd, 2) / (2**17)

  lon_index = _get_longitude_index(lonCprEven, lonCprOdd, zoneNum)

  numLonZoneEven = max(zoneNum, 1)
  numLonZoneOdd = max(zoneNum - 1, 1)

  lonZoneSizeEven = 360 / numLonZoneEven
  lonZoneSizeOdd = 360 / numLonZoneOdd

  lonEven = lonZoneSizeEven * (utils.modulo_function(lon_index, numLonZoneEven) + lonCprEven)
  lonOdd = lonZoneSizeOdd * (utils.modulo_function(lon_index, numLonZoneOdd) + lonCprOdd)

  # Technically should have logic to pick the most recent, but ADSB packets do not include a timestamp.
  longitude = lonOdd

  if(longitude >= 180 ):
    longitude -= 360

  return longitude

# Private methods

def _get_longitude_index(lonCprEven, lonCprOdd, zoneNum):
  x = lonCprEven * (zoneNum - 1)
  y = lonCprOdd * (zoneNum)
  lon_index = math.floor(x - y + 0.5)
  return lon_index
