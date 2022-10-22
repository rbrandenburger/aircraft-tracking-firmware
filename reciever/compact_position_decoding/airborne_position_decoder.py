
from .position_decoding_utilities import airborne_latitude_decoder, airborne_longitude_decoder

def get_airborne_position(evenBroadcast, oddBroadcast):

  encodedLatEven = evenBroadcast.encodedLatitude
  encodedLatOdd = oddBroadcast.encodedLatitude

  encodedLonEven = evenBroadcast.encodedLongitude
  encodedLonOdd = oddBroadcast.encodedLongitude

  #TODO: Catch ValueError
  latitude = airborne_latitude_decoder.get_latitude(encodedLatEven, encodedLatOdd)
  longitude = airborne_longitude_decoder.get_longitude(encodedLonEven, encodedLonOdd, latitude)

  return {
    "latitude" : latitude,
    "longitude" : longitude
  }