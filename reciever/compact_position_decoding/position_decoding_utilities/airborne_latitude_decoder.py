import math
import common_functions as utils

LAT_ZONE_SIZE_EVEN = 6.0
LAT_ZONE_SIZE_ODD = 6.10169491525

def get_latitude(cprEven, cprOdd):

  latCprEven = int(cprEven, 2) / (2**17)
  latCprOdd = int(cprOdd, 2) / (2**17)

  lat_index = get_latitude_index(latCprEven, latCprOdd)

  latEven = LAT_ZONE_SIZE_EVEN * (utils.modulo_function(lat_index, 60) + latCprEven)
  latOdd = LAT_ZONE_SIZE_ODD  * (utils.modulo_function(lat_index, 59) + latCprOdd)

  evenZoneNum = utils.get_longitude_zone_number(latEven)
  oddZoneNum = utils.get_longitude_zone_number(latOdd)

  if(evenZoneNum != oddZoneNum):
    raise ValueError("Zone numbers are not the same, likely cause by aircraft crossing over zones between broadcasts")

  #TODO: Implement Timestamp Decision
  return evenZoneNum

def get_latitude_index(latCprEven, latCprOdd):
  lat_index = math.floor(59 * latCprEven - 60 * latCprOdd + 0.5)
  return lat_index