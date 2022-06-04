# Author: Remington Brandenburger
# Date: April 2022

from . import number_base_converter
from .data_decoding import master_decoder

def generate_broadcast(rawBroadcast):
  
  #Convert raw hex data into binary
  binaryBroadcast = number_base_converter.convert_hex_to_binary(rawBroadcast)
  
  #Convert the binary broadcast data into a broadcast object
  broadcastObject = master_decoder.get_broadcast_from_binary(binaryBroadcast)

  return broadcastObject