# Author: Remington Brandenbugrer
# Date: April 2022

import csv

def read_data_from_file(filePath):

  data_row = []
  with open(filePath) as csvfile:
    
    reader = csv.reader(csvfile)
    for x in reader:
      data_row.append(x[0][1:-1].upper())
    
    return data_row