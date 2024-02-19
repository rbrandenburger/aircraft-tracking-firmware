from time import time
from telnetlib import Telnet
from dotenv import dotenv_values
import logger

ENV = dotenv_values(".env")
DUMP_1090_ADDRESS = ENV["DUMP_1090_ADDRESS"]
DUMP_1090_PORT = ENV["DUMP_1090_PORT"]


class Listener:
    def listen(broadcast_queue):
        conn = Telnet(DUMP_1090_ADDRESS, DUMP_1090_PORT)

        while True:
            try:
                broadcast = conn.read_until(b"\n", timeout=60).decode('ascii')
                broadcast_queue.put([broadcast, time()])
            except (ConnectionResetError, EOFError) as e:
                logger.log_error(e)

                # Try reconnecting
                conn = Telnet(DUMP_1090_ADDRESS, DUMP_1090_PORT)
