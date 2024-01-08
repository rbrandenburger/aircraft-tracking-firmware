import math
from . import shared_functions as utils

AIR_ZONE_SIZE_EVEN = 6.0
AIR_ZONE_SIZE_ODD = 6.10169491525

GROUND_ZONE_SIZE_EVEN = 1.5
GROUND_ZONE_SIZE_ODD = 1.52542373


def decode_airborne_latitude(cprEven, cprOdd):
    return _calculate(cprEven, cprOdd, AIR_ZONE_SIZE_EVEN, AIR_ZONE_SIZE_ODD)


def decode_surface_latitude(cprEven, cprOdd):
    return _calculate(cprEven, cprOdd, GROUND_ZONE_SIZE_EVEN, GROUND_ZONE_SIZE_ODD)


# Private methods

def _calculate(cprEven, cprOdd, zoneSizeEven, zoneSizeOdd):
    latCprEven = int(cprEven, 2) / (2**17)
    latCprOdd = int(cprOdd, 2) / (2**17)

    latIndex = _get_latitude_index(latCprEven, latCprOdd)

    latEven = zoneSizeEven * (utils.modulo_function(latIndex, 60) + latCprEven)
    latOdd = zoneSizeOdd * (utils.modulo_function(latIndex, 59) + latCprOdd)

    evenZoneNum = utils.get_longitude_zone_number(latEven)
    oddZoneNum = utils.get_longitude_zone_number(latOdd)

    if (evenZoneNum != oddZoneNum):
        raise ValueError("Zone numbers are not the same, likely caused by aircraft crossing over zones between broadcasts")

    # Technically should have logic to pick the most recent, but ADSB packets do not include a timestamp.
    return latOdd


def _get_latitude_index(latCprEven, latCprOdd):
    latIndex = math.floor(59 * latCprEven - 60 * latCprOdd + 0.5)
    return latIndex
