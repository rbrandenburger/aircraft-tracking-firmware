# Author: Remington Brandenburger
# Date: April 2022

from . import hex_to_binary as converter

def decode_data(broadcastDataList):

  convertedBroadcastList = []

  for broadcast in broadcastDataList:
    convertedBroadcastList.append(converter.convert_hex_to_binary(broadcast))

  for x in convertedBroadcastList:
    print(x)

  return 1