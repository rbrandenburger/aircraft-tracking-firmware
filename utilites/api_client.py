import httpx
from dotenv import dotenv_values

ENV = dotenv_values(".env")
AUTH_HEADER = {"x-api-key": ENV["API_KEY"]}


def post(broadcasts):
    response = httpx.post(ENV["API_URL"] + "/broadcasts/batch_create", headers=AUTH_HEADER, json=broadcasts)
    print(response)
    return
