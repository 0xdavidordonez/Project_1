###initial imports
import requests
import json
import os

url = "https://open-api.coinglass.com/public/v2/option?symbol=BTC"

headers = {
    "accept": "application/json",
    "coinglassSecret": "9e9d571c63b948e69bef2888b6fb9f27"
}

response = requests.get(url, headers=headers)

print(response.text)

# Formatting as json
data = response.json()

# Add indents to JSON and output to screen
print(json.dumps(data, indent=4))

