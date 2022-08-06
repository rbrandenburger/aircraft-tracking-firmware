# Author: Remington Brandenburger
# Description: main.py manages the function calling for the collection, processing, and uploading of data.
import sys
sys.dont_write_bytecode = True
import os
import raw_broadcast_loader
from broadcast_data_utilites import broadcast_object_generator
from broadcast_data_utilites import table_loader


if __name__ == '__main__':
  print('Running App...')

  #TODO: Tell radio to listen for airplanes ( 5 min duration )

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
    

  #TODO: Delete me
  for x in broadcasts:
    print(x)

  #TODO: Check for positional broadcasts and pair up even and odd frames and get coordinates
  #TODO: process list of broadcast objects, and update DB
  print('App processess completed')