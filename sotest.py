import requests
import uuid
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg1OTg5NDkzLCJpYXQiOjE3ODU5MDMwOTMsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDE3MDUwIn0.sz3bAfYZxf-uNnE_eG5HC7G9qEHZ5fAzOGXVyaPz8NApi4ORkbcQWK8o-V8PPewyCdFjYK9LVJxr037OSNwtqA"
CLIENT_ID = "1108017050"

BASE_URL = "https://api.dhan.co/v2"

# List of stock IDs you want to process
stock_ids = ['10300']

result_dict = {'10300': 'RAMASTEEL'}

def place_order(stockid):
    try:
        stock_name = result_dict[stockid]
        print(f"\nProcessing {stock_name} ({stockid}) ...")

        # Get LTP
        stock = yf.Ticker(f"{stock_name}.NS")
        ltp = stock.history(period="1d")['Close'][-1]

        # Define target, SL, and trail
        target = round(ltp + (ltp * 0.02), 2)  # 2% target
        sl = round(ltp - (ltp * 0.02), 2)      # 2% stop loss
        trail = round(ltp * 0.01, 2)           # 1% trailing jump

        payload = {
            "dhanClientId": CLIENT_ID,
            "transactionType": "BUY",
            "exchangeSegment": "NSE_EQ",
            "productType": "INTRADAY",
            "orderType": "MARKET",
            "securityId": stockid,
            "quantity": 1,
            "price": 0,
            #"targetPrice": target,
            "stopLossPrice": sl,
            "trailingJump": trail
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access-token": ACCESS_TOKEN
        }

        response = requests.post(f"{BASE_URL}/super/orders", headers=headers, json=payload)

        print(f"Order for {stock_name} placed: {response.json()}")
        return {stock_name: response.json()}

    except Exception as e:
        print(f"Error while processing {stockid}: {e}")
        return {stockid: "Failed"}

# Run in parallel threads
with ThreadPoolExecutor(max_workers=150) as executor:
    results = list(executor.map(place_order, stock_ids))

print("\nFinal Results:")
for r in results:
    print(r) #test
