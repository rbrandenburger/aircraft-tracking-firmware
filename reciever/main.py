# Author: Remington Brandenburger
# Description: main.py manages the function calling for the collection, processing, and uploading of data.
import sys, os
sys.dont_write_bytecode = True

from utilites import raw_broadcast_loader, raw_broadcast_decoder, coordinate_decoder
from utilites.general import table_loader

if __name__ == '__main__':
  print('Running App...')

  #TODO: Tell radio to listen for airplanes ( ? min duration )

  # Radio outputs broadcast data in CSV files
  currentPath = os.path.dirname(__file__)
  dataFilePath = os.path.join(currentPath, ".\\sample_data\\sample_data.csv")
  rawBroadcasts = raw_broadcast_loader.read_data_from_file(dataFilePath)
  aircraftLookupTable = table_loader.get_table("registeredAircraftTable.csv")

  # Decode and generate broadcast objects from raw hex data
  broadcasts = []
  for x in rawBroadcasts:
    broadcast = raw_broadcast_decoder.generate_broadcast_from_hex(x, aircraftLookupTable)
    if (broadcast != None):
      broadcasts.append(broadcast)

  # Positional broadcasts require additional decoding
  broadcasts = coordinate_decoder.decode_positions(broadcasts)

  #TODO: Delete me
  for x in broadcasts:
    print(x)
  
  #TODO: process list of broadcast objects, and update DB
  print('App processess completed')
