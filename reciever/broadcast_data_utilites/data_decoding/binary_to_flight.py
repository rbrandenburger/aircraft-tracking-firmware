from distutils.command.build import build
import os
from turtle import down
from .. import flight
import csv
from . import number_base_converter
from . import message_payload_decoder

def get_flight_from_binary(binaryString):

  downlinkFormat = get_downlink_format(binaryString[:5])

  transponderCa = get_transponder_capability(binaryString[5:8])

  registration = get_registration(binaryString[8:32])

  message = get_message(binaryString[32:88])

  print ("Registration Number: {}\nDownlink Format: {}\nTransponderCA: {}\n{}\n".format(registration, downlinkFormat, transponderCa, message))

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

  #TODO: Conver CSV into a database for faster searching.
  for row in lookupTable:
    if(hexAddress == row[0].upper()):
      return row[1]

  return "Undefined"

def get_message(binaryString):
  
  payloadDecoder = message_payload_decoder.PayloadDecoder
  typeCode = int(binaryString[:5], 2)
  
  match typeCode:

    case 1 | 2 | 3 | 4:
      #Type codes 1 through 4 are for aircraft identification
      payload = payloadDecoder.decode_aircraft_identification(binaryString, typeCode)
      return payload

    case 5 | 6 | 7 | 8:
      return "Surface Position"

    case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
      return "Airborne Position - Baro Altitude"

    case 19:
      return "Airborne Velocites"

    case 20 | 21 | 22:
      return "Airborne Position - GNSS Height"

    case 23 | 24 | 25 | 26 | 27:
      return "Reserved"

    case 28:
      return "Aircraft Status"

    case 29:
      return "Target state and status information"

    case 31:
      return "Aircraft Operation Status"

    case _:
      return "Undefined"
  
