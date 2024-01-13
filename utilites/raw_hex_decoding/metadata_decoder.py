from utilites.general import number_base_converter


def get_metadata(binaryString, aircraftLookupTable):
    metadata = dict()
    metadata['downlinkFormat'] = _get_downlink_format(binaryString[:5])
    metadata['transponderCa'] = _get_transponder_capability(binaryString[5:8])
    metadata['icao24'] = _get_icao_24(binaryString[8:32])
    metadata['aircraftDetails'] = _get_aircraft_details(metadata['icao24'], aircraftLookupTable)

    return metadata


# Private methods


def _get_downlink_format(binaryString):
    downlinkFormat = int(binaryString, 2)
    return downlinkFormat


def _get_transponder_capability(binaryString):
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


def _get_icao_24(binaryString):
    return number_base_converter.convert_binary_to_hex(binaryString)


def _get_aircraft_details(icao24, aircraftLookupTable):
    for row in aircraftLookupTable:
        if (icao24 == row[0].upper()):
            return {"registrationNumber": row[1], "manufacturer": row[3], "model": row[4]}

    return None
