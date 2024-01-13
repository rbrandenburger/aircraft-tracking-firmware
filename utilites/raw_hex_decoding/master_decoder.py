from . import payload_decoder, metadata_decoder
from objects import broadcast
import logger


class DecodingError(Exception):
    pass


def get_broadcast_from_binary(binaryString, aircraftLookupTable):
    try:
        broadcastMetadata = metadata_decoder.get_metadata(binaryString[:32], aircraftLookupTable)

        if (broadcastMetadata['downlinkFormat'] != 17):  # Downlink format must be 17 for civilian ADSB broadcasts
            return None
        else:
            downlinkFormat = broadcastMetadata['downlinkFormat']
            transponderCa = broadcastMetadata['transponderCa']
            icao24 = broadcastMetadata['icao24']
            aircraftDetails = broadcastMetadata['aircraftDetails']
            payload = payload_decoder.get_payload(binaryString[32:88])
    except DecodingError as e:
        logger.log_error(e)
        return None

    return broadcast.Broadcast(
        downlinkFormat=downlinkFormat,
        transponderCapability=transponderCa,
        icao24=icao24,
        aircraftDetails=aircraftDetails,
        payload=payload
    )
