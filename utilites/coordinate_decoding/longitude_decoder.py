from . import shared_functions as utils
import math

AIR_ZONE_SIZE = 360
SURFACE_ZONE_SIZE = 90


def decode_airborne_longitude(cprEven, cprOdd, latitude):
    return _decode_longitude(cprEven, cprOdd, latitude, AIR_ZONE_SIZE)


def decode_surface_longitude(cprEven, cprOdd, latitude):
    return _decode_longitude(cprEven, cprOdd, latitude, SURFACE_ZONE_SIZE)


# Private methods

def _decode_longitude(cprEven, cprOdd, latitude, totalZoneSize):
    zoneNum = utils.get_longitude_zone_number(latitude)

    lonCprEven = int(cprEven, 2) / (2**17)
    lonCprOdd = int(cprOdd, 2) / (2**17)

    lonIndex = _get_longitude_index(lonCprEven, lonCprOdd, zoneNum)

    numLonZoneEven = max(zoneNum, 1)
    numLonZoneOdd = max(zoneNum - 1, 1)

    lonZoneSizeEven = totalZoneSize / numLonZoneEven
    lonZoneSizeOdd = totalZoneSize / numLonZoneOdd

    lonEven = lonZoneSizeEven * (utils.modulo_function(lonIndex, numLonZoneEven) + lonCprEven)
    lonOdd = lonZoneSizeOdd * (utils.modulo_function(lonIndex, numLonZoneOdd) + lonCprOdd)

    # Technically should have logic to pick the most recent, but ADSB packets do not include a timestamp.
    longitude = lonOdd

    if (longitude >= 180):
        longitude -= 360

    return longitude


def _get_longitude_index(lonCprEven, lonCprOdd, zoneNum):
    x = lonCprEven * (zoneNum - 1)
    y = lonCprOdd * (zoneNum)
    lon_index = math.floor(x - y + 0.5)
    return lon_index
