"""
Title: Financial Data Collection and Storage
Author: Jasmine Sharron
Date: 01 August 2023
Purpose: To automate the process of collecting, cleaning, and storing data 
from financial APIs such as Alpha Vantage.
"""

# Import appropriate libraries.
import requests
import pandas as pd
from datetime import datetime
import sqlite3

class FinancialDataCollector:
    def __init__(self, api_key, ticker_symbol, function="TIME_SERIES_DAILY", output_size="full", datatype="json"):
        self.api_key = api_key
        self.ticker_symbol = ticker_symbol
        self.function = function
        self.output_size = output_size
        self.datatype = datatype
        self.data = None
    
    def get_data(self):
        # Define the API endpoint and parameters
        base_url = "https://www.alphavantage.co/query?"
        params = {
            "function": self.function,      # Alterable based on type of data desired 
            "symbol": self.ticker_symbol,   # Stock ticker
            "outputsize": self.output_size, # "compact" or "full" depending on the amt of historical data desired
            "datatype": self.datatype,      # "json" or "csv" depening on format desired
            "apikey": self.api_key
        }
        
        # Send GET request to API
        response = requests.get(base_url, params=params)
        
        # IF the request was successful, store the data
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(f"Unable to fetch data, HTTP Status Code: {response.status_code}")
    
    def clean_data(self):
        # Extract the relevant data
        data = self.data['Time Series (Daily)']
        
        # Convert the data to a DataFrame and transpose it
        df = pd.DataFrame(data).T
        
        # Change the columns' data type to float and rename them
        df = df.astype(float)
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        
        # Store the cleaned data
        self.data = df
    
    def store_data(self, file_format="csv"):
        # Generate the file name using the current date and ticker symbol
        date_str = datetime.now().strftime('%Y_%m_%d')
        file_name = f"{self.ticker_symbol}_{date_str}"
        
        # Store the data in the selected format
        if file_format == 'csv':
            self.data.to_csv(f"{file_name}.csv")
        elif file_format == 'json':
            self.data.to_json(f"{file_name}.json")
        elif file_format == 'db':
            conn = sqlite3.connect(f"{file_name}.db")
            self.data.to_sql(self.ticker_symbol, conn)
        else:
            print(f"Unsupported file format: {file_format}")
        
        print("\nData has been saved as a", file_format)  # Confirm that the data has been saved

def main():
    # Define the stock symbol and the API key
    ticker_symbol = <"stock_ticker">
    api_key = <"your_API_key">
    
    # Create an instance of FinancialDataCollector 
    collector = FinancialDataCollector(api_key, ticker_symbol)
    
    # Collect data
    collector.get_data()
    # print("Data after get_data:\n", collector.data)
    
    # Clean data
    collector.clean_data()
    print("\nData after clean_data:\n", collector.data.head())
    
    # Store data
    collector.store_data()
    
if __name__ == "__main__":
    main()
