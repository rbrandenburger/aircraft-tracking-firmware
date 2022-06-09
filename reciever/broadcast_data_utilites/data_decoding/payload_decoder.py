# Author: Remington Brandenbugrer
# Date: April 2022
# Calls correct decoding util based on passed through typecode

from .payload_decoding_utilities import aircraft_id_decoder as IdDecoder
from .payload_decoding_utilities import airborne_velocity_decoder as velocities_decoder

def get_payload(binaryString):

  typeCode = int(binaryString[:5], 2)
  payload = {}

  match typeCode:

    case 1 | 2 | 3 | 4:
      payload['messageType'] = "aircraft_identification"
      payload.update(IdDecoder.decode_aircraft_identification(typeCode, binaryString))
      return payload
    
    case 5 | 6 | 7 | 8:
      return "Surface Position"

    case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
      return "Airborne Position - Baro Altitude"

    case 19:
      payload['messageType'] = "airborne_velocities"
      payload.update(velocities_decoder.decode_airborne_velocities(typeCode, binaryString))
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
      payload = "Undefined"

  return payload
      



