# robo-advisor

A Python application that automates the process of providing clients with stock trading recommendations. The system provides three types of recommendations to the client: BUY, HOLD, or SELL. The system also provides insight on the stock's most recent quarterly fundamental data as well as a stock price chart. 

# Prerequisites 

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](http://github.com/pk664/robo-advisor) under your own control, then "clone" or download your remote copy onto your local computer.

After cloning the repo, navigate there from the command-line:

```sh
cd robo-advisor
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

## Security Requirements Setup 

In in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to specify your API Key to issue requests to the AlphaVantage API. For example: 

    ALPHAVANTAGE_API_KEY="abc123"

## Recommendation Criteria 

If the stock is trading at a 20% premium compared to its most recent high, then the stock will be regarded a SELL. This would be a great time for users to take profits. 

If the stock is trading at a 20% discount compared to its most recent low, then the stock will be regarded a BUY. This would be a great time for users to buy in. 

If the stock is flutuating in between the range between 20% from its most recent low to 20% from its most recent high, then the stock will be regarded a HOLD. 

## Robo Advisor Insights Explained 

The following definitions of financial metrics are adapted from Investopedia. 

Fundamental data provided by the Robo Advisor application include: forward price to earnings ratio, beta, price to book ratio, enterprise value to revenue, enterprise value to EBITDA, and dividend yield. These financial metrics are intended to help inform the user with additional information regarding their stock of interest. 

+ Forward P/E ratio indicates the market value of a stock compared to the companies future earnings. 
+ Beta indicates how volatile a stock's price is compared to the overall stock market. 
+ Price to Book ratio compares the company's market value to its book value, which represents the net assets of a company. 
+ Enterprise Value to Revenue measures how much it would cost to purchase a company's value in terms of its revenue. 
+ Enterprsie Value to EBITDA measures how much it would cost to purchase a company's value in terms of its earnings before interest, taxes, depreciation, and amortization. 
+ Dividend Yield indicates how much a company pays out in dividends each year relative to its stock price. 

## Usage 

Run the Robo Advisor application by executing the following command below. Happy Investing! 

> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", 
it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment.

```py
python app/robo_advisor.py




