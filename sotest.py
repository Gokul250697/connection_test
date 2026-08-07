import requests
import yfinance as yf
import traceback
from concurrent.futures import ThreadPoolExecutor

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg2MTYxMTAxLCJpYXQiOjE3ODYwNzQ3MDEsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDE3MDUwIn0.VGn17A0DCSNab6v1jkLyeiQ2FCEzQEGdRo4pbUiKy2gppayXg1deZ0l5wYlXd4ZLSIg17L64K_cTOi5Pj1dT8w"
CLIENT_ID = "1108017050"

BASE_URL = "https://api.dhan.co/v2"

stock_ids = ["11787", "10188"]

result_dict = {
    "11787": "GOYALALUM",
    "10188": "SHYAMCENT"
}

def place_order(stockid):
    try:
        stock_name = result_dict[stockid]
        print(f"\nProcessing {stock_name} ({stockid})...")

        # Get LTP
        stock = yf.Ticker(f"{stock_name}.NS")

        hist = stock.history(period="1d")

        print("\nYahoo Finance Data:")
        print(hist)

        if hist.empty:
            print("No data received from Yahoo Finance")
            return {stockid: "No Data"}

        ltp = hist["Close"].iloc[-1]

        print(f"LTP: {ltp}")

        # Calculate Target / SL / Trail
        target = round(ltp + (ltp * 0.02), 2)
        sl = round(ltp - (ltp * 0.02), 2)
        trail = round(ltp * 0.01, 2)

        print(f"Target: {target}")
        print(f"Stop Loss: {sl}")
        print(f"Trailing Jump: {trail}")

        payload = {
            "dhanClientId": CLIENT_ID,
            "transactionType": "BUY",
            "exchangeSegment": "NSE_EQ",
            "productType": "INTRADAY",
            "orderType": "MARKET",
            "securityId": stockid,
            "quantity": 1,
            "price": 0,
            "targetPrice": target,
            "stopLossPrice": sl,
            "trailingJump": trail
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access-token": ACCESS_TOKEN
        }

        print("\nSending request to Dhan...")
        print("Payload:", payload)

        response = requests.post(
            f"{BASE_URL}/super/orders",
            headers=headers,
            json=payload
        )

        print("\nHTTP Status:", response.status_code)
        print("Raw Response:")
        print(response.text)

        try:
            print("JSON Response:")
            print(response.json())
            return {stock_name: response.json()}
        except Exception:
            print("Response is not JSON")
            return {stock_name: response.text}

    except Exception:
        print("\n========== EXCEPTION ==========")
        traceback.print_exc()
        print("===============================")
        return {stockid: "Failed"}

# Execute
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(place_order, stock_ids))

print("\nFinal Results:")
for r in results:
    print(r)