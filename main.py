# Author: Remington Brandenburger
# Description: main.py manages the function calling for the collection, processing, and uploading of data.
import sys, os
sys.dont_write_bytecode = True

from utilites import raw_broadcast_loader, raw_broadcast_decoder, coordinate_decoder, api_client
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

  #TODO: POST broadcasts to app API
  # for broadcast in broadcasts:
  #   print(broadcast)
    
  api_client.post(broadcasts)
  
  #TODO: Loop instead of terminate
  print('App processess completed')
