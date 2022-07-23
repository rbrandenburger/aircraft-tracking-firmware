import logging
import datetime

def log_error(message):
  fileName = "logs/" + str(datetime.date.today()) + ".log"
  timestamp = datetime.datetime.now().strftime("\nLocal System Time: %Y-%m-%dT%H:%M:%S:%f")
  logging.basicConfig(filename=fileName, filemode='a')
  logging.error(timestamp + str(message))

def log_warning(message):
  fileName = "logs/" + str(datetime.date.today()) + ".log"
  timestamp = datetime.datetime.now().strftime("\nLocal System Time: %Y-%m-%dT%H:%M:%S:%f")
  logging.basicConfig(filename=fileName, filemode='a')
  logging.warning(timestamp + str(message))
