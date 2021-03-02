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
import seaborn as sns 

def to_usd(my_price):
    return f"${my_price:,.2f}" 


#
# INFO INPUTS 
#

# This code was adapted from Prof Rossetti's screencast 

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
    else: 
        break


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

# TODO
#while True:
#    if symbol not in parsed_response:
#        print("Oops, invalid input.")
#        break
#    else: 
#        break
#
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
# STOCK PRICE GRAPH 
# 

# create a dataframe of the time series data, where we have a row per day
# write the dataframe to csv and chart it with dataframe friendly dataviz packages 

from pandas import DataFrame 

line_df = DataFrame(tsd)

# CONVERT DATA FRAME TO CSV 
#line_df.to_csv('tsd.csv')

# READ CSV 

x = pd.read_csv("tsd.csv")


#for index, row in x.iterrows(): 
#    print(line_df.loc[3,:])


#ns.lineplot(data=line_df, x="date", y="stock_price_usd")



#
# RESULTS 
#

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


