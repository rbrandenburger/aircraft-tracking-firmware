from time import sleep
from utilites import api_client
import logger

SECONDS_BETWEEN_BATCH = 10


class Sender:
    def batch_send_broadcasts(processedBroadcastQueue):
        while True:
            try:
                sleep(SECONDS_BETWEEN_BATCH)

                processedBroadcasts = []

                while not processedBroadcastQueue.empty():
                    broadcast = processedBroadcastQueue.get()
                    processedBroadcasts.append(broadcast.serialize())

                api_client.post(processedBroadcasts)
            except Exception as e:
                msg = "Processed Broadcasts: {}\n".format(processedBroadcasts)
                e.args = (e.args[0] + msg,) + e.args[1:]
                logger.log_error(e)
                continue
