from time import sleep
from utilites import api_client

SECONDS_BETWEEN_BATCH = 10


class Sender:
    def batch_send_broadcasts(processedBroadcastQueue):
        while True:
            sleep(SECONDS_BETWEEN_BATCH)

            processedBroadcasts = []

            while not processedBroadcastQueue.empty():
                processedBroadcasts.append(processedBroadcastQueue.get())

            api_client.post(processedBroadcasts)
