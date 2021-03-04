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
# TODO: how to make displayed symbols be capital letters

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

while True: 
    symbol = input("Please input a stock ticker:")
    if symbol.isnumeric() == True: 
        print("Oops, that's an invalid input. Please run the program again and enter a valid stock ticker.")
        exit()
    elif len(symbol) > 4: 
        print("Oops, that's an invalid input. Please run the program again and enter a valid stock ticker.")
        exit()
    else: 
        break

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

# TODO: SORT TO ENSURE LATEST DATE IS FIRST 
# especially if data structure changes later on. This assumes first day is on top 

#dates.sort() 
#sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates] 

#
#latest_day = sorteddates[0]
#

# TODO: 52-WEEK HIGHS AND LOWS 
#request_url_monthly = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&{symbol}=IBM&apikey={api_key}"
#response_monthly = requests.get(request_url_monthly)
#parsed_response_monthly = json.loads(response_monthly.text)

#ft_week_high = parsed_response_monthly["52WeekHigh"]
#ft_week_low = parsed_response_monthly["52WeekLow"]

# TODO: REQUESTING FUNDAMENTAL DATA 
request_url_fundamentals = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
response_fundamentals = requests.get(request_url_fundamentals)
parsed_response_fundamentals = json.loads(response_fundamentals.text)

industry = parsed_response_fundamentals["Industry"]
forward_pe = parsed_response_fundamentals["ForwardPE"]
analyst_target = parsed_response_fundamentals["AnalystTargetPrice"]

# OTHER STUFF 

latest_day = dates[0]
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

#
# INFO OUTPUTS 
#

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

#
# RESULTS 
#

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("-------------------------")
print(f"INDUSTRY: {industry}")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"52-WEEK HIGH: {to_usd(float(recent_high))}")
print(f"52-WEEK LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"FORWARD P/E RATIO: {forward_pe}")
print(f"ANALYST PRICE TARGET: {analyst_target}")

# Change this from using 100 days recent low to 52-week high 

if float(latest_close) < 1.2*float(recent_low): 
    print("RECOMMENDATION: BUY")
    print("The stock is trading at a discount. Now would be a great time to enter.")
elif float(latest_close) > 1.2*float(recent_high):
    print("RECOMMENDATION: SELL")
    print("The stock is trading at a premium. Now would be a great time to take profits.")
else: 
    print("RECOMMENDATION: HOLD")
    print("The stock is fluctuating sideways. Keep holding.")


print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("Happy Investing!")
print("-------------------------")

#
# STOCK PRICE GRAPH 
# 

from pandas import DataFrame 
df = pd.read_csv(csv_file_path)

sns.lineplot(data=df[["timestamp", "close"]], x="timestamp", y="close")
plt.title(f"{symbol} Price Graph")
plt.ylabel("Stock Price")
plt.xlabel("Time")
plt.show()



