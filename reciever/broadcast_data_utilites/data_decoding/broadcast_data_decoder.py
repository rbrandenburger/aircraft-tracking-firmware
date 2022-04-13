# Author: Remington Brandenburger
# Date: April 2022

#TODO: Change from list input to single item input
from . import number_base_converter as hexConverter
from . import binary_to_flight as binaryConverter

from .. import flight

def decode_data(broadcastDataList):

  convertedBroadcastList = []
  collectedFlights = []

  for hexBroadcast in broadcastDataList:
    convertedBroadcastList.append(hexConverter.convert_hex_to_binary(hexBroadcast))
  
  for binaryBroadcast in convertedBroadcastList:
    collectedFlights.append(binaryConverter.get_flight_from_binary(binaryBroadcast))

  return 1