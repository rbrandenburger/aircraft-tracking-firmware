import multiprocessing
from listener import Listener
from processor import Processor

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")

    broadcast_queue = multiprocessing.SimpleQueue()

    listen_process = multiprocessing.Process(target=Listener.listen, args=[broadcast_queue])
    listen_process.start()

    processor_process = multiprocessing.Process(target=Processor.process_broadcasts, args=[broadcast_queue])
    processor_process.start()
