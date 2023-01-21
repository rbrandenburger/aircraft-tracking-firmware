# Author: Remington Brandenburger
# Description: main.py manages the function calling for the collection, processing, and uploading of data.
import sys, os
sys.dont_write_bytecode = True

import raw_broadcast_loader
from broadcast_data_utilites import broadcast_object_generator, table_loader
from compact_position_decoding import airborne_position_decoder


if __name__ == '__main__':
  print('Running App...')

  #TODO: Tell radio to listen for airplanes ( ? min duration )

  #SDR outputs broadcast data in CSV files
  currentPath = os.path.dirname(__file__)
  dataFilePath = os.path.join(currentPath, ".\\sample_data\\sample_data.csv")
  rawBroadcasts = raw_broadcast_loader.read_data_from_file(dataFilePath)
  aircraftLookupTable = table_loader.get_table("registeredAircraftTable.csv")

  #Generate broadcast objects from raw hex data
  broadcasts = []
  for x in rawBroadcasts:
    broadcast = broadcast_object_generator.generate_broadcast(x, aircraftLookupTable)
    if (broadcast != None):
      broadcasts.append(broadcast)

  #TODO: Surface positions
  broadcasts = airborne_position_decoder.decode_positions(broadcasts)
    

  #TODO: Delete me
  for x in broadcasts:
    print(x)
  
  #TODO: process list of broadcast objects, and update DB
  print('App processess completed')
