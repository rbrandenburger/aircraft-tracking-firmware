# Author: Remington Brandenbugrer
# Date: April 2022
# Calls correct decoding util based on passed through typecode

from .payload_decoding_utils import aircraft_id_decoder as IdDecoder

class PayloadDecoder:

  def __init__(self):
    return

  def getPayload(typeCode, binaryString):

    payload = ""

    match typeCode:

      case 1 | 2 | 3 | 4:
        payload = IdDecoder.decode_aircraft_identification(typeCode, binaryString)
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
        payload = "Undefinedd"

    return payload
        

  

