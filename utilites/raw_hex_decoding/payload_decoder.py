from .payload_decoding_utilities import aircraft_id_decoder
from .payload_decoding_utilities import airborne_velocity_decoder
from .payload_decoding_utilities import airborne_position_decoder
from .payload_decoding_utilities import surface_position_decoder

def get_payload(binaryString):
  typeCode = int(binaryString[:5], 2)
  payload = {'typeCode' : typeCode}

  match typeCode:
    case 1 | 2 | 3 | 4:
      payload['messageType'] = "aircraftIdentification"
      payload.update(aircraft_id_decoder.decode_aircraft_identification(typeCode, binaryString))
      return payload
    
    case 5 | 6 | 7 | 8:
      payload['messageType'] = "surfacePosition"
      payload.update(surface_position_decoder.decode_surface_postion(binaryString))
      return payload

    case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 20 | 21 | 22:
      payload['messageType'] = "airbornePosition"
      payload['typeCode'] = typeCode
      payload.update(airborne_position_decoder.decode_airborne_postition(typeCode, binaryString))
      return payload

    case 19:
      payload['messageType'] = "airborneVelocities"
      payload.update(airborne_velocity_decoder.decode_airborne_velocities(binaryString))
      return payload

    case 23 | 24 | 25 | 26 | 27:
      payload['messageType'] = "reserved"
      return payload

    case 28:
      payload['messageType'] = "aircraftStatus"
      return payload

    case 29:
      payload['messageType'] = "targetStateAndStatusInfo"
      return payload

    case 31:
      payload['messageType'] = "aircraftOperationStatus"
      return payload

    case _:
      payload['messageType'] = "Undefined"

  return payload
