from .payload_decoding_utilities import aircraft_id_decoder
from .payload_decoding_utilities import airborne_velocity_decoder
from .payload_decoding_utilities import airborne_position_decoder
from .payload_decoding_utilities import surface_position_decoder

def get_payload(binaryString):
  typeCode = int(binaryString[:5], 2)
  payload = {}

  match typeCode:
    case 1 | 2 | 3 | 4:
      payload['messageType'] = "aircraft_identification"
      payload.update(aircraft_id_decoder.decode_aircraft_identification(typeCode, binaryString))
      return payload
    
    case 5 | 6 | 7 | 8:
      payload['messageType'] = "surface_position"
      payload.update(surface_position_decoder.decode_surface_postion(binaryString))
      return payload

    case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 20 | 21 | 22:
      payload['messageType'] = "airborne_position"
      payload['typeCode'] = typeCode
      payload.update(airborne_position_decoder.decode_airborne_postition(typeCode, binaryString))
      return payload

    case 19:
      payload['messageType'] = "airborne_velocities"
      payload.update(airborne_velocity_decoder.decode_airborne_velocities(binaryString))
      return payload

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
      



