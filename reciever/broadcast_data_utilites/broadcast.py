class Broadcast:
  def __init__(self, downlinkFormat, transponderCapability, registrationNum, payload):
    self.downlinkFormat = downlinkFormat
    self.transponderCapability = transponderCapability
    self.registrationNum = registrationNum
    self.payload = payload

  def __str__(self):
    return "Registration Number: {}\nDownlink Format: {}\nTransponderCA: {}\n{}\n".format(self.registrationNum, self.downlinkFormat, self.transponderCapability, self.payload)