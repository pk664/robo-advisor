# this is the "app/robo_advisor.py" file

import requests
import json
from datetime import datetime

now = datetime.now()

#
# INFO INPUTS 
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"


response = requests.get(request_url)
#print(response.status_code) # 200, which corresponds to the part of the HTML request
#print(response.text) #actual body of the response we'll get back, which is a dictionary like object 


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_close = parsed_response["Time Series(Daily)"]) ["2021-02-28"]
breakpoint() 

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
print(f"LATEST CLOSE: {latest_close}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")