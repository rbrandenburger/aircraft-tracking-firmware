from . import number_base_converter
from .raw_data_decoding import master_decoder
import logger

def generate_broadcast(rawBroadcast, aircraftLookupTable):
  #Convert raw hex data into binary
  binaryBroadcast = number_base_converter.convert_hex_to_binary(rawBroadcast)
  if(len(binaryBroadcast) < 112):
    return None

  #Convert the binary broadcast data into a broadcast object
  broadcastObject = master_decoder.get_broadcast_from_binary(binaryBroadcast, aircraftLookupTable)

  return broadcastObject