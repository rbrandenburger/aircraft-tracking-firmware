from .coordinate_decoding import latitude_decoder, longitude_decoder
import logger
import geocoder

SURFACE_POSITION_TYPECODES = [5, 6, 7, 8, 9]
AIRBORNE_POSITION_TYPECODES = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22]
POSITIONAL_TYPECODES = SURFACE_POSITION_TYPECODES + AIRBORNE_POSITION_TYPECODES
LOCAL_COORDINATES = geocoder.ip('me').latlng


def decode_positions(broadcasts):
    positionalBroadcasts, otherBroadcasts = _seperate_positional_broadcasts(broadcasts)

    encodedAirPositionPairs = _pair_positional_broadcasts(positionalBroadcasts, AIRBORNE_POSITION_TYPECODES)
    encodedSurfacePositionPairs = _pair_positional_broadcasts(positionalBroadcasts, SURFACE_POSITION_TYPECODES)

    decodedAirPositionBroadcasts = _decode_pairs(encodedAirPositionPairs, isSurface=False)
    decodedSurfacePositionBroadcasts = _decode_pairs(encodedSurfacePositionPairs, isSurface=True)

    decodedBroadcasts = decodedAirPositionBroadcasts + decodedSurfacePositionBroadcasts + otherBroadcasts
    return decodedBroadcasts


# Private methods


def _seperate_positional_broadcasts(broadcasts):
    positionalBroadcasts = []
    otherBroadcasts = []

    for broadcast in broadcasts:
        if broadcast.payload['typeCode'] in POSITIONAL_TYPECODES:
            positionalBroadcasts.append(broadcast)
        else:
            otherBroadcasts.append(broadcast)

    return positionalBroadcasts, otherBroadcasts


def _decode_pairs(encodedPairs, isSurface=False):
    decodedPairs = []
    for _, broadcastPair in encodedPairs.items():
        decodedBroadcast = _get_decoded_broadcast(broadcastPair, isSurface)

        if isSurface:
            decodedBroadcast = _correct_for_relative_position(decodedBroadcast)

        decodedPairs.append(decodedBroadcast)

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

    try:
        latitude = _get_latitude(evenBroadcast, oddBroadcast, isSurface)
        longitude = _get_longitude(evenBroadcast, oddBroadcast, latitude, isSurface)
    except ValueError as e:
        msg = "\nBroadcast even:\n{}\nBroadcast odd:\n{}".format(evenBroadcast, oddBroadcast)
        e.args = (e.args[0] + msg,) + e.args[1:]  # This just appends msg to the ValueError message
        logger.log_error(e)
        return

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

    for broadcast in broadcasts:
        if broadcast.payload['typeCode'] not in typeCodes:
            continue
        elif broadcast.registrationNumber in pairs:
            pairs[broadcast.registrationNumber].append(broadcast)
        else:
            pairs[broadcast.registrationNumber] = [broadcast]

    # Verify that there are 2 broadcasts to calculate position
    for aircraft in pairs.copy():
        if len(pairs[aircraft]) != 2:
            del pairs[aircraft]  # TODO add a cache for the next batch of broadcast

    return pairs


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
