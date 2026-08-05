import requests

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg1OTg5NDkzLCJpYXQiOjE3ODU5MDMwOTMsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDE3MDUwIn0.sz3bAfYZxf-uNnE_eG5HC7G9qEHZ5fAzOGXVyaPz8NApi4ORkbcQWK8o-V8PPewyCdFjYK9LVJxr037OSNwtqA"
CLIENT_ID = "1108017050"

import requests

qty = 1
stockid = "15347"

BASE_URL = "https://api.dhan.co/v2"

url = f"{BASE_URL}/orders"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "access-token": ACCESS_TOKEN
}

payload = {
    "dhanClientId": CLIENT_ID,
    "transactionType": "BUY",
    "exchangeSegment": "NSE_EQ",
    "productType": "INTRADAY",
    "orderType": "MARKET",
    "validity": "DAY",
    "securityId": stockid,
    "quantity": qty,
    "price": 0,
    "triggerPrice": 0,
    "afterMarketOrder": False,
    "amoTime": "OPEN",
    "disclosedQuantity": 0
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.json())