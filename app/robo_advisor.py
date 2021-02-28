# this is the "app/robo_advisor.py" file

import requests
import json
from datetime import datetime

now = datetime.now()

def to_usd(my_price):
    return f"${my_price:,.2f}" 


#
# INFO INPUTS 
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"


response = requests.get(request_url)
#print(response.status_code) # 200, which corresponds to the part of the HTML request
#print(response.text) #actual body of the response we'll get back, which is a dictionary like object 


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: sort to ensure latest day is first 
# especially if data structure changes later on. This assumes first day is on top 

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]



#max of all 100 day prices 
high_prices = [ ]

for date in dates: 
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))

recent_high = max(high_prices)

#min of all 100 day prices 

low_prices = [ ]

for date in dates: 
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_low = min(low_prices)

#
# INFO OUTPUTS 
#


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
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
print("HAPPY INVESTING!")
print("-------------------------")