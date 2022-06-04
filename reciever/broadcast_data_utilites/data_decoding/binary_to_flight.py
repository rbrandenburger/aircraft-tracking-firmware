from distutils.command.build import build
import os
from turtle import down
from .. import flight
import csv
from .. import number_base_converter
from . import message_payload_decoder

def get_flight_from_binary(binaryString):

  downlinkFormat = get_downlink_format(binaryString[:5])

  transponderCa = get_transponder_capability(binaryString[5:8])

  registration = get_registration(binaryString[8:32])

  payload = get_payload(binaryString[32:88])

  print ("Registration Number: {}\nDownlink Format: {}\nTransponderCA: {}\n{}\n".format(registration, downlinkFormat, transponderCa, payload))

def get_downlink_format(binaryString):

  downlinkFormat = int(binaryString, 2)
  return downlinkFormat

def get_transponder_capability(binaryString):

  capability = int(binaryString, 2)

  match capability:

    case 0:
      return "Level 1"
    case 1 | 2 | 3:
      return "Reserved"
    case 4:
      return "Level 2+ with ability to set CA to 7; ground"
    case 5:
      return "Level 2+ with ability to set CA to 7; airborne"
    case 6:
      return "Level 2+ with ability to set CA to 7; either ground or airborne"
    case 7:
      return "Downlink request value is 0, or the Flight Status is 2, 3, 4, or 5; either airborne or on the ground"
    case _:
      return "Error: Undefined"

def get_registration(binaryString):
  hexAddress = number_base_converter.convert_binary_to_hex(binaryString)

  currentPath = os.path.dirname(__file__)
  newPath = os.path.join(currentPath, ".\\tables\\registeredAircraftTable.csv")
  lookupTable = csv.reader(open(newPath, "r"), delimiter=",")

  #Looking up flight in CSV flight tables
  #TODO: Load CSV into memory for faster searching.
  for row in lookupTable:
    if(hexAddress == row[0].upper()):
      return row[1]

  return "Undefined"

def get_payload(binaryString):
  
  typeCode = int(binaryString[:5], 2)
  payloadDecoder = message_payload_decoder.PayloadDecoder
  payload = payloadDecoder.getPayload(typeCode, binaryString)
  return payload
