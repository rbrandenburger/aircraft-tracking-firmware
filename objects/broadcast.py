class Broadcast:
    def __init__(self, downlinkFormat, transponderCapability, registrationNumber, payload):
        self.downlinkFormat = downlinkFormat
        self.transponderCapability = transponderCapability
        self.registrationNumber = registrationNumber
        self.payload = payload

    def __str__(self):
        return "Registration Number: {}\nDownlink Format: {}\nTransponderCA: {}\nPayload: {}\n".format(self.registrationNumber, self.downlinkFormat, self.transponderCapability, self.payload)

    def serialize(self):
        return self.__dict__
