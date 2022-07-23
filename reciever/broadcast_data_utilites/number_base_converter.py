hexToBinaryTable = {
  '0' : '0000',
  '1' : '0001',
  '2' : '0010',
  '3' : '0011',
  '4' : '0100',
  '5' : '0101',
  '6' : '0110',
  '7' : '0111',
  '8' : '1000',
  '9' : '1001',
  'A' : '1010',
  'B' : '1011',
  'C' : '1100',
  'D' : '1101',
  'E' : '1110',
  'F' : '1111'
}

def convert_hex_to_binary(hexString):
  binaryString = ""
  for c in hexString:
    bits = hexToBinaryTable[c]
    binaryString += bits

  return binaryString

def convert_binary_to_hex(binaryString):
  hexList = list(hexToBinaryTable.keys())
  binaryList = list(hexToBinaryTable.values())
  hexString = ""

  while (len(binaryString) > 0):
    subString = binaryString[:4]
    position = binaryList.index(subString)
    hexString += hexList[position]
    binaryString = binaryString[4:]

  return hexString
  
  