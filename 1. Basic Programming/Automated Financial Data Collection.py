#!/usr/bin/env python
# coding: utf-8

# # Automated Financial Data Collection
#
# ## Overview
# A script automating the process of collecting, cleaning, and storing data from financial API, Alpha Vantage.

# ### 1. Set Up Environment
# Import appropriate libraries.
import requests
import json
import pandas as pd
import sqlite3

# Get API key from Alpha Vantage
API_KEY = 'CD265QP86PO56Z9U'

# ### 2. Collect Data: Define the data retrieval function.
def get_stock_data(symbol, API_KEY):
    base_url = "https://www.alphavantage.co/query?"
    function = "TIME_SERIES_DAILY" # Alterable based on the data desired. 
    output_size = "compact" # Choice b/w "compact" or "full" depending on the amt of historical data desired.
    datatype = "json"
    
    # Construct the API request URL
    api_url = f"{base_url}function={function}&symbol={symbol}&outputsize={output_size}&apikey={API_KEY}&datatype={datatype}"
    
    # Send request to API
    response = requests.get(api_url)
    
    # Parse the generated JSON response
    data = json.loads(response.text)
    
    return data

# Test 1:
# get_stock_data("AAPL", API_KEY)


# ### 3. Data Cleaning: Clean and pre-process the data to make it suitable for analysis.
def clean_data(raw_data):
    
    # Convert gathered data into a Pandas DataFrame
    data = pd.DataFrame(raw_data['Time Series (Daily)']).T
    
    # Rename columns
    data.columns = ["Open", "High", "Low", "Close", "Volume"]
    
    # Convert index to datetime
    data.index = pd.to_datetime(data.index)
    
    # Convert data to numeric values
    for column in data.columns:
        data[column] = pd.to_numeric(data[column])

    return data

# Test 2
clean_data(get_stock_data("AAPL", API_KEY))


# ### 4. Data Storage: Save the cleaned data into a local file or database for future use.
def store_data(data, symbol, db_path):
    conn = sqlite3.connect(db_path)
    
    # Write the data to a sqlite table
    data.to_sql(symbol, conn, if_exists='replace', index=True)

    conn.close()


# ### 5. Run Script: Test on Apple stock data.
def main():
    
    # Define the stock symbol and the API key
    symbol = "AAPL"
    api_key = "CD265QP86PO56Z9U"
    db_path = "stock_data.db"

    # Collect data
    raw_data = get_stock_data(symbol, api_key)

    # Clean data
    data = clean_data(raw_data)

    # Store data
    store_data(data, symbol, db_path)
    
if __name__ == "__main__":
    main()




