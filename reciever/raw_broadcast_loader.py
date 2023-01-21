import csv
import re

def read_data_from_file(filePath):
  data_row = []
  with open(filePath) as csvfile:
    
    reader = csv.reader(csvfile)
    for x in reader:
      if(x): #<- If x is not empty
        data_row.append(re.sub(r'[^0-9a-fA-F]','',x[0].upper())) #Using re to remove non hex chars
    
    return data_row
