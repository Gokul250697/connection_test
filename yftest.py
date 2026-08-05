import yfinance as yf

stock = yf.Ticker("RAMASTEEL.NS")

hist = stock.history(period="1d")

print(hist)
print("Empty:", hist.empty)