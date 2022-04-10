from distutils.command.build import build
import os
from turtle import down
from .. import flight
import csv
from . import number_base_converter

def get_flight_from_binary(binaryString):

  downlinkFormat = get_downlink_format(binaryString[:5])

  transponderCa = get_transponder_capability(binaryString[5:8])

  address = get_address(binaryString[8:32])

  print ("Downlink Format: {} --- TransponderCA: {} --- Flight Number: {}".format(downlinkFormat, transponderCa, address))

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

def get_address(binaryString):
  hexAddress = number_base_converter.convert_binary_to_hex(binaryString)

  currentPath = os.path.dirname(__file__)
  newPath = os.path.join(currentPath, ".\\aircraft_lookup_table\\aircraftTable.csv")
  lookupTable = csv.reader(open(newPath, "r"), delimiter=",")

  #TODO: Conver CSV into a database for faster searching.
  for row in lookupTable:
    if(hexAddress == row[0].upper()):
      return row[1]

  return "Undefined"
  
