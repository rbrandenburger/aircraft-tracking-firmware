import logging
import datetime
import os

def log_error(message):
  _verify_directory()
  fileName = "./logs/" + str(datetime.date.today()) + ".log"
  logging.basicConfig(filename=fileName, filemode='a')
  logging.error(str(message))

def log_warning(message):
  _verify_directory()
  fileName = "./logs/" + str(datetime.date.today()) + ".log"
  logging.basicConfig(filename=fileName, filemode='a', format='\n%(levelname)s %(asctime)s\n%(message)s')
  logging.warning(str(message))

# Private methods

def _verify_directory():
  path = "./logs/"
  if not os.path.exists(path):
    os.makedirs(path)
  return
