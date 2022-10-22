import math
NUM_LAT_ZONES = 15

def get_longitude_zone_number(latitude):
  if(latitude == 0 or latitude >= 87 or latitude <= -87):
    return get_longitude_zone_edge_case(latitude)
  else:
    innerNumerator = 1 - math.cos(math.pi/(2 * NUM_LAT_ZONES))
    innerDenominator = (math.cos((math.pi / 180) * latitude))**2

    outerNumerator = 2 * math.pi
    outerDenominator = math.acos(1 - (innerNumerator / innerDenominator))

    zoneNumber = math.floor(outerNumerator / outerDenominator)
    return zoneNumber

def get_longitude_zone_edge_case(latitude):
  if (latitude == 0):
    return 59
  elif(latitude == 87 or latitude == -87):
    return 2
  else:
    return 1


def modulo_function(x, y):
  if (y != 0):
    val = x - y * math.floor(x/y)
    return val
  else:
    return None