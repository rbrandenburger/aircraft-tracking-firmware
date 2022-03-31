# Author: Remington Brandenburger
# Date: April 2022
# Description: main.py manages the function calling for the collection, processing, and uploading of data.


import broadcast_data_utilites.csv_reader as csv_reader
import broadcast_data_utilites.data_decoding.data_decoder as decoder

if __name__ == '__main__':
  print('Running App...')

  #TODO: Tell radio to listen for airplanes ( 5 min duration )

  #TODO: Decode .CSV file and create flight objects
  #SDR outputs broadcast data in CSV files
  filePath = '.\sample_data\sample_data.csv'
  encodedBroadcastList = csv_reader.read_data_from_file(filePath)

  decodedData = decoder.decode_data(encodedBroadcastList)

  #TODO: Upload flights to database
  print('App processess completed')