# this is the "app/robo_advisor.py" file

import requests
import csv 
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
now = datetime.now()

def to_usd(my_price):
    return f"${my_price:,.2f}" 


#
# INFO INPUTS 
#

# TODO: CAPTURE DATA IF USER INPUTS A NON VALID TICKER 
# TODO: line graph for stock price 
# TODO: create a reason for recomendation 




api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


while True: 
    symbol = input("Please input a stock or cryptocurrency ticker:")
    if symbol.isnumeric() == True: 
        print("Oops, that's an invalid input. Please enter a properly-formed stock symbol like 'MSFT'.")
    elif len(symbol) > 4: 
        print("Oops, that's an invalid input. Please enter a properly-formed stock symbol like 'MSFT'.")
#    elif symbol not in parsed_response["Meta Data"]:
#       print("Oops, that's an invalid input. Please enter a properly-formed stock symbol like 'MSFT'.")
    else: 
        break


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: sort to ensure latest day is first 
# especially if data structure changes later on. This assumes first day is on top 

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
# RECOMMENDATION
# 

# If a stock price is 20% less than its recent low, then buy 
# If not, then don't buy 


#
# LINE GRAPH OF STOCK PRICES OVER TIME 
# This code was adapted from @joe297 on Plotly 

#df = px.data.gapminder().query("country=='Canada'")
#fig = px.line(df, x="date", y="price", title='{symbol} Stock Price')
#fig.show()
#
#import plotly.plotly as py
#from plotly.graph_objs import *
#
#stock_price = {
#  "line": {
#    "color": "rgba(31,119,180,1)", 
#    "fillcolor": "rgba(31,119,180,1)"
#  }, 
#  "mode": "lines", 
#  "name": "{symbol}", 
#  "type": "scatter", 
#  "x": [ ]
#  "y": [ ]
#  "xaxis": "x", 
#  "yaxis": "y"
#}

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")


if float(latest_close) <= 0.9*float(recent_low): 
    print("RECOMMENDATION: BUY")
else: 
    print("RECOMMENDATION: DON'T BUY")


print("RECOMMENDATION REASON: The stock is not trading at less than 10 percent of its recent low. Now's not a great time to buy.")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("Happy Investing!")
print("-------------------------")


