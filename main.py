from googlesearch import search
import json

with open("config.json", "r") as f:
    config = json.load(f)

print(config)