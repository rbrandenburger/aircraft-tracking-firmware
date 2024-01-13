import multiprocessing
from listener import Listener
from processor import Processor
from sender import Sender

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")

    hexBroadcastQueue = multiprocessing.SimpleQueue()
    processedBroadcastQueue = multiprocessing.SimpleQueue()

    listen_process = multiprocessing.Process(
        target=Listener.listen,
        args=[hexBroadcastQueue]
    )
    listen_process.start()

    processor_process = multiprocessing.Process(
        target=Processor.process_broadcasts,
        args=[hexBroadcastQueue, processedBroadcastQueue]
    )
    processor_process.start()

    sender_process = multiprocessing.Process(
        target=Sender.batch_send_broadcasts,
        args=[processedBroadcastQueue]
    )
    sender_process.start()

    listen_process.join()
    processor_process.join()
    sender_process.join()
