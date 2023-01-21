
from .position_decoding_utilities import airborne_latitude_decoder, airborne_longitude_decoder
import logger

def decode_positions(broadcasts):
  decoded_broadcasts = []
  encoded_positional_broadcasts = []

  for broadcast in broadcasts:
    if (broadcast.payload['messageType'] == 'airborne_position'):
      encoded_positional_broadcasts.append(broadcast)
    else:
      decoded_broadcasts.append(broadcast)

  paired_broadcasts = _pair_positional_broadcasts(encoded_positional_broadcasts)

  for _, value in paired_broadcasts.items():
    decoded_broadcasts.append( _get_decoded_broadcast(value) )

  return decoded_broadcasts

# Private methods

def _pair_positional_broadcasts(broadcasts):
  pairs = {}

  for broadcast in broadcasts:
    if broadcast.registrationNum in pairs:
      pairs[broadcast.registrationNum].append(broadcast)
    else:
      pairs[broadcast.registrationNum] = [broadcast]

  for registrationNum in pairs.copy():
    if len(pairs[registrationNum]) != 2:
      del pairs[registrationNum] #TODO add a cache for the next batch of broadcast
  
  return pairs

def _get_decoded_broadcast(broadcast_pair):
  coordinates = _get_airborne_position(broadcast_pair)

  if coordinates == None: return

  broadcast_pair[1].payload['latitude'] = coordinates['latitude']
  broadcast_pair[1].payload['longitude'] = coordinates['longitude']
  
  return broadcast_pair[1]

def _get_airborne_position(broadcasts):
  if broadcasts[0].payload['cprFormat'] ==  '0':
    evenBroadcast = broadcasts[0]
    oddBroadcast = broadcasts[1]
  else:
    evenBroadcast = broadcasts[1]
    oddBroadcast = broadcasts[0]

  try:
    latitude = _get_latitude(evenBroadcast, oddBroadcast)
    longitude = _get_longitude(evenBroadcast, oddBroadcast, latitude)
  except ValueError as e:
    msg = "\nBroadcast even:\n{}\nBroadcast odd:\n{}".format(evenBroadcast, oddBroadcast)
    e.args = (e.args[0] + msg,) + e.args[1:] # This just appends msg to the ValueError message
    logger.log_error(e)
    return

  return {
    "latitude" : latitude,
    "longitude" : longitude
  }

def _get_latitude(evenBroadcast, oddBroadcast):
  encodedLatEven = evenBroadcast.payload['encodedLatitude']
  encodedLatOdd = oddBroadcast.payload['encodedLatitude']

  return airborne_latitude_decoder.decode_latitude(encodedLatEven, encodedLatOdd)

def _get_longitude(evenBroadcast, oddBroadcast, latitude):
  encodedLonEven = evenBroadcast.payload['encodedLongitude']
  encodedLonOdd = oddBroadcast.payload['encodedLongitude']

  return airborne_longitude_decoder.decode_longitude(encodedLonEven, encodedLonOdd, latitude)
