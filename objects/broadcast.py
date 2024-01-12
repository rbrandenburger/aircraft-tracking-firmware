class Broadcast:
    def __init__(self, downlinkFormat, transponderCapability, registrationNumber, payload, timestamp=None):
        self.downlinkFormat = downlinkFormat
        self.transponderCapability = transponderCapability
        self.registrationNumber = registrationNumber
        self.payload = payload
        self.timestamp = timestamp

    def __str__(self):
        return "Registration Number: {}\nDownlink Format: {}\nTransponderCA: {}\nPayload: {}\nRecieved At: {}".format(
            self.registrationNumber,
            self.downlinkFormat,
            self.transponderCapability,
            self.payload,
            self.timestamp
        )

    def serialize(self):
        return self.__dict__
