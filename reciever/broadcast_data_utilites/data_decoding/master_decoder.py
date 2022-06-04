from turtle import down
from . import payload_decoder
from . import metadata_decoder
from .. import broadcast

def get_broadcast_from_binary(binaryString):

  #Metadata included in a broadcast contains downlink format, transponder capability, and registration number
  flightMetadata = metadata_decoder.get_metadata(binaryString[:32])

  downlinkFormat = flightMetadata['downlinkFormat']

  transponderCa = flightMetadata['transponderCa']

  registration = flightMetadata['registration']

  #Now to get the message's payload
  payload = payload_decoder.get_payload(binaryString[32:88])

  return broadcast.Broadcast(downlinkFormat, transponderCa, registration, payload)

