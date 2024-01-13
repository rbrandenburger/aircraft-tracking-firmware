from .coordinate_decoding import latitude_decoder, longitude_decoder

import logger
import geocoder
from time import time

SURFACE_POSITION_TYPECODES = [5, 6, 7, 8, 9]
AIRBORNE_POSITION_TYPECODES = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22]
POSITIONAL_TYPECODES = SURFACE_POSITION_TYPECODES + AIRBORNE_POSITION_TYPECODES
LOCAL_COORDINATES = geocoder.ip('me').latlng


class DecodingError(Exception):
    pass


def decode_positions(positionalBroadcasts):
    encodedAirPositionPairs, unpaired_air_broadcasts = _pair_positional_broadcasts(positionalBroadcasts, AIRBORNE_POSITION_TYPECODES)
    encodedSurfacePositionPairs, unpaired_surface_broadcasts = _pair_positional_broadcasts(positionalBroadcasts, SURFACE_POSITION_TYPECODES)

    decodedAirPositionBroadcasts = _decode_pairs(encodedAirPositionPairs, isSurface=False)
    decodedSurfacePositionBroadcasts = _decode_pairs(encodedSurfacePositionPairs, isSurface=True)

    decodedBroadcasts = decodedAirPositionBroadcasts + decodedSurfacePositionBroadcasts
    return decodedBroadcasts, unpaired_air_broadcasts + unpaired_surface_broadcasts


# Private methods


def _decode_pairs(encodedPairs, isSurface=False):
    decodedPairs = []

    for _, broadcastPair in encodedPairs.items():
        try:
            decodedBroadcast = _get_decoded_broadcast(broadcastPair, isSurface)
            if isSurface:
                decodedBroadcast = _correct_for_relative_position(decodedBroadcast)
            decodedPairs.append(decodedBroadcast)
        except DecodingError as e:
            msg = "\nBroadcast 0:\n{}\nBroadcast 1:\n{}".format(broadcastPair[0], broadcastPair[1])
            e.args = (e.args[0] + msg,) + e.args[1:]  # Append 'msg' to error message
            logger.log_error(e)
            continue

    return decodedPairs


def _get_decoded_broadcast(broadcastPair, isSurface):
    coordinates = _get_coordinates(broadcastPair, isSurface)

    if coordinates is None:
        return

    broadcastPair[1].payload['latitude'] = coordinates['latitude']
    broadcastPair[1].payload['longitude'] = coordinates['longitude']

    return broadcastPair[1]


def _get_coordinates(broadcasts, isSurface):
    if broadcasts[0].payload['cprFormat'] == '0':
        evenBroadcast = broadcasts[0]
        oddBroadcast = broadcasts[1]
    else:
        evenBroadcast = broadcasts[1]
        oddBroadcast = broadcasts[0]

    latitude = _get_latitude(evenBroadcast, oddBroadcast, isSurface)
    longitude = _get_longitude(evenBroadcast, oddBroadcast, latitude, isSurface)

    return {
        "latitude": latitude,
        "longitude": longitude
    }


def _get_latitude(evenBroadcast, oddBroadcast, isSurface):
    encodedLatEven = evenBroadcast.payload['encodedLatitude']
    encodedLatOdd = oddBroadcast.payload['encodedLatitude']

    if (isSurface):
        return latitude_decoder.decode_surface_latitude(encodedLatEven, encodedLatOdd)
    else:
        return latitude_decoder.decode_airborne_latitude(encodedLatEven, encodedLatOdd)


def _get_longitude(evenBroadcast, oddBroadcast, latitude, isSurface):
    encodedLonEven = evenBroadcast.payload['encodedLongitude']
    encodedLonOdd = oddBroadcast.payload['encodedLongitude']

    if (isSurface):
        return longitude_decoder.decode_surface_longitude(encodedLonEven, encodedLonOdd, latitude)
    else:
        return longitude_decoder.decode_airborne_longitude(encodedLonEven, encodedLonOdd, latitude)


def _pair_positional_broadcasts(broadcasts, typeCodes):
    pairs = {}
    unpaired_broadcasts = []

    for broadcast in broadcasts:
        icao24 = broadcast.icao24

        if broadcast.payload['typeCode'] not in typeCodes:
            continue
        elif icao24 in pairs:
            # We must have both CPR formats, otherwise just replace the old broadcast
            if pairs[icao24][0].payload["cprFormat"] != broadcast.payload["cprFormat"]:
                pairs[icao24].append(broadcast)
            else:
                pairs[icao24][0] = broadcast
        else:
            pairs[icao24] = [broadcast]

    for aircraft in pairs.copy():
        if len(pairs[aircraft]) != 2:
            # If the broadcast is younger than a minute, keep it around in case it's partner comes in
            if (time() - pairs[aircraft][0].timestamp < 60):
                unpaired_broadcasts.append(pairs[aircraft][0])
            del pairs[aircraft]

    return pairs, unpaired_broadcasts


def _correct_for_relative_position(broadcast):
    correctedLat = _find_closest_lat(broadcast.payload['latitude'])
    correctedLon = _find_closest_lon(broadcast.payload['longitude'])

    broadcast.payload['latitude'] = correctedLat
    broadcast.payload['longitude'] = correctedLon

    return broadcast


def _find_closest_lat(latitude):
    northernLat = southernLat = difNorth = difSouth = None

    if _in_northern_hemisphere:
        northernLat = latitude
        southernLat = latitude - 90
    else:
        southernLat = latitude
        northernLat = latitude + 90

    difNorth = abs(northernLat - LOCAL_COORDINATES[0])
    difSouth = abs(southernLat - LOCAL_COORDINATES[0])

    if difNorth < difSouth:
        return northernLat
    else:
        return southernLat


def _find_closest_lon(longitude):
    quadOne = longitude
    quadTwo = (longitude + 90) % 360
    quadThree = (longitude + 180) % 360
    quadFour = (longitude + 270) % 360

    possibilities = [quadOne, quadTwo, quadThree, quadFour]

    differences = lambda possibilities: abs(possibilities - LOCAL_COORDINATES[1])

    return min(possibilities, key=differences)


def _in_northern_hemisphere():
    if LOCAL_COORDINATES[0] > 0:
        return True
    else:
        return False
