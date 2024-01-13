class Broadcast:
    def __init__(self, downlinkFormat, transponderCapability, icao24, aircraftDetails, payload, timestamp=None):
        self.downlinkFormat = downlinkFormat
        self.transponderCapability = transponderCapability
        self.icao24 = icao24
        self.aircraftDetails = aircraftDetails
        self.payload = payload
        self.timestamp = timestamp

    def __str__(self):
        return "ICAO24 Code: {}\nAircraft Details: {}\nDownlink Format: {}\nTransponder Capability: {}\nPayload: {}\nRecieved At: {}\n".format(
            self.icao24,
            self.aircraftDetails,
            self.downlinkFormat,
            self.transponderCapability,
            self.payload,
            self.timestamp
        )

    def serialize(self):
        return self.__dict__
