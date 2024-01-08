from . import payload_decoder, metadata_decoder
from objects import broadcast
import logger


def get_broadcast_from_binary(binaryString, aircraftLookupTable):
    broadcastMetadata = metadata_decoder.get_metadata(binaryString[:32], aircraftLookupTable)

    if (broadcastMetadata['downlinkFormat'] != 17):  # Downlink format must be 17 for civilian ADSB broadcasts
        logger.log_warning(str.format("Downlink Format not 17\nBroadcast: {}", binaryString))
        return None
    else:
        downlinkFormat = broadcastMetadata['downlinkFormat']
        transponderCa = broadcastMetadata['transponderCa']
        registration = broadcastMetadata['registration']
        payload = payload_decoder.get_payload(binaryString[32:88])

    return broadcast.Broadcast(downlinkFormat, transponderCa, registration, payload)
