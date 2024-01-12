from time import time
from telnetlib import Telnet
from dotenv import dotenv_values

ENV = dotenv_values(".env")
DUMP_1090_ADDRESS = ENV["DUMP_1090_ADDRESS"]
DUMP_1090_PORT = ENV["DUMP_1090_PORT"]


class Listener:
    def listen(broadcast_queue):
        with Telnet(DUMP_1090_ADDRESS, DUMP_1090_PORT) as conn:
            while True:
                broadcast = conn.read_until(b"\n").decode('ascii')
                broadcast_queue.put([broadcast, time()])
