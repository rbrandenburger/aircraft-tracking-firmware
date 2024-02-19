from utilites.general import table_loader
from utilites import (
    raw_broadcast_loader,
    hex_broadcast_decoder,
    coordinate_decoder,
    # api_client
)

import os
import re


if __name__ == '__main__':
    print('Running App...')

    # Radio outputs broadcast data in CSV files
    currentPath = os.path.dirname(__file__)
    dataFilePath = os.path.join(currentPath, ".\\sample_data\\sample_data_2.csv")
    rawBroadcasts = raw_broadcast_loader.read_data_from_file(dataFilePath)
    aircraftLookupTable = table_loader.get_table("registeredAircraftTable.csv")

    # Decode and generate broadcast objects from raw hex data
    incompletePositionalBroadcasts = []
    for hexBroadcast in rawBroadcasts:
        hexBroadcast = re.sub(r'[^0-9a-fA-F]', '', hexBroadcast.upper())
        broadcast = hex_broadcast_decoder.generate_broadcast_from_hex(hexBroadcast, aircraftLookupTable)

        if (broadcast is None):
            continue

        # If it was a positional packet, add to positional array and run positional decoder
        elif broadcast.payload['typeCode'] in coordinate_decoder.POSITIONAL_TYPECODES:
            incompletePositionalBroadcasts.append(broadcast)
            broadcasts, incompletePositionalBroadcasts = coordinate_decoder.decode_positions(incompletePositionalBroadcasts)

            if (len(broadcasts) == 0):
                continue

            for broadcast in broadcasts:
                print(broadcast)
                # add broadcast to api queue

        else:
            continue
            # add broadcast to api queue
            # print(broadcast)

    # TODO: Loop instead of terminate
    print('App processess completed')
