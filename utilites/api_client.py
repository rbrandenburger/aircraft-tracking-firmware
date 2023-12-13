import httpx
from dotenv import dotenv_values

ENV = dotenv_values(".env")
AUTH_HEADER = {"x-api-key": ENV["API_KEY"]}

def post(broadcasts):
  for broadcast in broadcasts:
    r = httpx.post(ENV["API_URL"] + "/broadcasts/create", json = broadcast.serialize(), headers=AUTH_HEADER)
  return
