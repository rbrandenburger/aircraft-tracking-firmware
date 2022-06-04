# Author: Remington Brandenburger
# Date: April 2022
# Description: main.py manages the function calling for the collection, processing, and uploading of data.


import raw_broadcast_loader as rawBroadcastLoader
from broadcast_data_utilites import flight_object_generator as flightGenerator
import os

if __name__ == '__main__':
  print('Running App...')

  print('test')

  #TODO: Tell radio to listen for airplanes ( 5 min duration )

  #TODO: Decode .CSV file and create flight objects
  #SDR outputs broadcast data in CSV files
  currentPath = os.path.dirname(__file__)
  dataFilePath = os.path.join(currentPath, ".\\sample_data\\sample_data.csv")
  encodedBroadcastList = rawBroadcastLoader.read_data_from_file(dataFilePath)

  flights = flightGenerator.generate_flights(encodedBroadcastList)

  #TODO: Upload flights to database
  print('App processess completed')