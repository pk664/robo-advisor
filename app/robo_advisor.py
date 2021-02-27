# this is the "app/robo_advisor.py" file

import requests
import json

#
# INFO INPUTS 
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"


response = requests.get(request_url)
#print(response.status_code) # 200, which corresponds to the part of the HTML request
#print(response.text) #actual body of the response we'll get back, which is a dictionary like object 


parsed_response = json.loads(response.text)

breakpoint() 




#
# INFO OUTPUTS 
#


#print("-------------------------")
#print("SELECTED SYMBOL: XYZ")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: 2018-02-20 02:00pm")
#print("-------------------------")
#print("LATEST DAY: 2018-02-20")
#print("LATEST CLOSE: $100,000.00")
#print("RECENT HIGH: $101,000.00")
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")