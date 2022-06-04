# Author: Remington Brandenburger
# Date: April 2022

#TODO: Change from list input to single item input
from . import number_base_converter as hexConverter
from .data_decoding import binary_to_flight as binaryConverter

from . import flight

def generate_flights(broadcastDataList):

  convertedBroadcastList = []
  collectedFlights = []

  #Convert raw hex data into binary
  for hexBroadcast in broadcastDataList:
    convertedBroadcastList.append(hexConverter.convert_hex_to_binary(hexBroadcast))
  
  #Convert the binary broadcast data into flight objects
  for binaryBroadcast in convertedBroadcastList:
    collectedFlights.append(binaryConverter.get_flight_from_binary(binaryBroadcast))

  return collectedFlights