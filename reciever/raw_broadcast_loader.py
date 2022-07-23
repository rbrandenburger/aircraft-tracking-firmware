import csv
import re

def read_data_from_file(filePath):
  data_row = []
  with open(filePath) as csvfile:
    
    reader = csv.reader(csvfile)
    for x in reader:
      data_row.append(re.sub(r'[\W_]','',x[0].upper())) #Using re to remove non alphanumeric chars
    
    return data_row