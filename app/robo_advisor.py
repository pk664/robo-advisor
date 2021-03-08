# this is the "app/robo_advisor.py" file

import requests
import csv 
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
now = datetime.now()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
def to_usd(my_price):
    return f"${my_price:,.2f}" 

# This code was adapted from Prof Rossetti's screencast 

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

while True: 
    symbol = input("Please input a stock ticker:")
    if symbol.isnumeric() == True: 
        print("Oops, that's an invalid input. Please run the program again and enter a valid stock ticker.")
        exit()
    elif len(symbol) > 5: 
        print("Oops, that's an invalid input. Please run the program again and enter a valid stock ticker.")
        exit()
    else: 
        break

# REQUESTING TIME SERIES DAILY DATA 
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

while True: 
    if "Error Message" in response.text: 
        print("Oops, that's an invalid input. Please run the program again and enter a valid stock ticker.")
        exit()
    else: 
        break 

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) 
dates.sort()

# REQUESTING FUNDAMENTAL DATA 
request_url_fundamentals = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
response_fundamentals = requests.get(request_url_fundamentals)
parsed_response_fundamentals = json.loads(response_fundamentals.text)

industry = parsed_response_fundamentals["Industry"]
forward_pe = parsed_response_fundamentals["ForwardPE"]
beta = parsed_response_fundamentals["Beta"]
price_to_book_ratio = parsed_response_fundamentals["PriceToBookRatio"]
ev_to_revenue = parsed_response_fundamentals["EVToRevenue"]
ev_to_ebitda = parsed_response_fundamentals["EVToEBITDA"]
dividend_yield = parsed_response_fundamentals["DividendYield"]

# SORTING DATES 
latest_day = dates[-1]
latest_close = tsd[latest_day]["4. close"]

high_prices = [ ]
low_prices = [ ]

for date in dates: 
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
recent_high = max(high_prices)
recent_low = min(low_prices)

# INFO OUTPUTS 
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() 
    for date in dates: 
        daily_prices = tsd[date] 
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["6. volume"]
        })


# RESULTS 
print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print(f"REQUESTING STOCK MARKET DATA AT:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("-------------------------")
print(f"INDUSTRY: {industry}")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSING PRICE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECENT QUARTERLY FUNDAMENTAL DATA:")
print(f"FORWARD P/E RATIO: {forward_pe}")
while True: 
    if beta == str('None'): 
        break
    else: 
        print(f"BETA: {beta}")
        break 
print(f"PRICE TO BOOK RATIO: {price_to_book_ratio}")
print(f"EV/REVENUE: {ev_to_revenue}")
print(f"EV/EBITDA: {ev_to_ebitda}") 
while True: 
    if dividend_yield == str('None'): 
        break 
    else:
        dividend_yield_percentage = float(dividend_yield)*100
        print(f"DIVIDEND YIELD: {dividend_yield_percentage}%")
        break 
print("-------------------------")
print("ROBO ADVISOR INSIGHTS")

# BUY HOLD OR SELL 
if float(latest_close) < 0.8*float(recent_low): 
    print("Recommendation: BUY")
    print(f"The stock is trading at a 20% discount compared to its 100-day recent low.")
    print("Now would be a great time to enter.")
elif float(latest_close) > 1.2*float(recent_high):
    print("Recommendation: SELL")
    print("The stock is trading at a 20% premium compared to its 100-day recent high.")
    print("Now would be a great time to take profits.")
else: 
    print("Recommendation: HOLD")
    print("The stock is fluctuating sideways.")
    print("It has not broken recent highs nor recent lows.")
    print("Now would be a great time to keep holding the stock.")


print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("Happy Investing!")

# STOCK PRICE GRAPH 
from pandas import DataFrame 

# Bryan Zhou helped me with this line of code 
df = pd.read_csv(csv_file_path)

sns.lineplot(data=df[["timestamp", "close"]], x="timestamp", y="close")
plt.title(f"{symbol} Price Graph")
plt.ylabel("Stock Price")
plt.xlabel("Time")
plt.show()

