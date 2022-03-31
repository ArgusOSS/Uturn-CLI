import json
import os

server_dir = os.path.dirname(os.path.realpath(__file__))[:-8]

with open(server_dir + "/config.json", "r") as file:
    json_read = json.loads(file.read())

token = json_read.get("token")
ip = json_read.get("IP")