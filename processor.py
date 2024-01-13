import logger
import re
from utilites.general import table_loader
from utilites import (
    hex_broadcast_decoder,
    coordinate_decoder,
)


class Processor:
    def process_broadcasts(hexBroadcastQueue, processedBroadcastQueue):
        incompletePositionalBroadcasts = []

        aircraftLookupTable = table_loader.get_table("registeredAircraftTable.csv")

        while True:
            try:
                hexBroadcast, timestamp = hexBroadcastQueue.get()
                hexBroadcast = re.sub(r'[^0-9a-fA-F]', '', hexBroadcast.upper())
                broadcast = hex_broadcast_decoder.generate_broadcast_from_hex(hexBroadcast, aircraftLookupTable)

                # When the captured radio broadcast is not an ADSB packet
                if (broadcast is None):
                    continue

                broadcast.timestamp = timestamp

                # If it was a positional packet, add to positional array and run positional decoder
                if broadcast.payload['typeCode'] in coordinate_decoder.POSITIONAL_TYPECODES:
                    incompletePositionalBroadcasts.append(broadcast)
                    broadcasts, incompletePositionalBroadcasts = coordinate_decoder.decode_positions(incompletePositionalBroadcasts)

                    if (len(broadcasts) == 0):
                        continue

                    for broadcast in broadcasts:
                        processedBroadcastQueue.put(broadcast)

                else:
                    processedBroadcastQueue.put(broadcast)

            except Exception as e:
                # Append broadcast data to error message
                msg = "\nBroadcast: {}".format(hexBroadcast)
                e.args = (e.args[0] + msg,) + e.args[1:]

                logger.log_error(e)
                continue
