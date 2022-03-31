import csv

def read_data_from_file(filePath):

  capturedBroadcasts = []
  with open(filePath) as csvfile:
    
    reader = csv.reader(csvfile)
    for row in reader:
      capturedBroadcasts.append(row[0][1:-1])
    
    for x in capturedBroadcasts:
      print(x) #TODO: Delete this
    
    return capturedBroadcasts

def decode_data ():
  print('Hello')
