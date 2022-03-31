# Author: Remington Brandenbugrer
# Date: April 2022

import csv

def read_data_from_file(filePath):

  capturedBroadcasts = []
  with open(filePath) as csvfile:
    
    reader = csv.reader(csvfile)
    for row in reader:
      capturedBroadcasts.append(row[0][1:-1].upper())
    
    return capturedBroadcasts