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
# If ticker has more than 4 letters, if ticker has a number in it 
# If ticker isnumeric but also has letters 


while True: 
    symbol = input("Please input a stock or cryptocurrency ticker:")
    if symbol.isnumeric() == True: 
        print("Oops, that's an invalid input. Please try again!")
    elif len(symbol) > 4: 
        print("Oops, that's an invalid input. Please try again!")
    else: 
        break

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

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
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


