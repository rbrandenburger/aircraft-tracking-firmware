from . import payload_decoder
from . import metadata_decoder
from .. import broadcast
import logger

def get_broadcast_from_binary(binaryString, aircraftLookupTable):
  flightMetadata = metadata_decoder.get_metadata(binaryString[:32], aircraftLookupTable)

  if( flightMetadata['downlinkFormat'] != 17 ):   #Downlink format must be 17 for civilian ADSB broadcasts
    print(str.format("\nCAUTION: Downlink Format not 17 for: {}\n",binaryString))
    return None
  else:
    downlinkFormat = flightMetadata['downlinkFormat']
    transponderCa = flightMetadata['transponderCa']
    registration = flightMetadata['registration']
    payload = payload_decoder.get_payload(binaryString[32:88])

    return broadcast.Broadcast(downlinkFormat, transponderCa, registration, payload)

