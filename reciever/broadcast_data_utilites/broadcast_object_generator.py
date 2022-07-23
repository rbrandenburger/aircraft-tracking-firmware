from . import number_base_converter
from .data_decoding import master_decoder
import logger

def generate_broadcast(rawBroadcast, aircraftLookupTable):
  #Convert raw hex data into binary
  try:
    binaryBroadcast = number_base_converter.convert_hex_to_binary(rawBroadcast)
  except Exception:
    error = str.format("\nFile: broadcast_object_generator.py\nMessage: Issue converting hex to binary\nHex Broadcast: {}\n",rawBroadcast)
    logger.log_error(error)

    return None
  
  #Convert the binary broadcast data into a broadcast object
  broadcastObject = master_decoder.get_broadcast_from_binary(binaryBroadcast, aircraftLookupTable)

  return broadcastObject