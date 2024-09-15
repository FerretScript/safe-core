import requests
import pandas as pd
import time
import json
import os

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = '87Z74N17MP35PME1'

# List of companies (free API symbols)
symbols = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'META', 'MDB', 'WMT', 'COST', 
           'KR', 'T', 'FDX', 'DIS', 'BA', 'LMT', 'IBM', 'SORIANA.B', 'OSK']  # Apple, Google, Tesla, Microsoft

# Base URL for Alpha Vantage API
BASE_URL = 'https://www.alphavantage.co/query'

# Function to retrieve time series data
def get_time_series_data(symbol, api_key):
    params = {
        'function': 'TIME_SERIES_DAILY',  # Retrieves daily time series data
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact',  # 'compact' for last 100 data points; 'full' for full-length data
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'Time Series (Daily)' in data:
            # Extract the time series data
            time_series = data['Time Series (Daily)']

            # Convert the time series into a DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')

            # Rename the columns for clarity
            df.rename(columns={
                '1. open': 'Open',
                '2. high': 'High',
                '3. low': 'Low',
                '4. close': 'Close',
                '5. volume': 'Volume'
            }, inplace=True)

            # Convert the index to datetime
            df.index = pd.to_datetime(df.index)

            # Convert data types to numeric
            df = df.astype(float)

            # Sort the DataFrame by date
            df.sort_index(inplace=True)

            return df.to_dict()  # Return as dictionary for saving in JSON
        else:
            print("Time series data not found in the response.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to retrieve company overview (fundamental data)
def get_company_overview(symbol, api_key):
    params = {
        'function': 'OVERVIEW',  # Retrieves company overview
        'symbol': symbol,
        'apikey': api_key,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            print("Company overview not found in the response.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to process and save data for each company
def process_company_data(symbol, api_key):
    print(f"\nProcessing data for {symbol}...")

    # Create a dictionary to store both time series and overview data
    company_data = {}

    # Retrieve time series data
    time_series_data = get_time_series_data(symbol, api_key)
    if time_series_data:
        company_data['time_series'] = time_series_data

    # Retrieve company overview
    company_overview = get_company_overview(symbol, api_key)
    if company_overview:
        company_data['overview'] = company_overview

    # Save the data to a .json file
    if company_data:
        # Create directory for the data if it doesn't exist
        if not os.path.exists('company_data'):
            os.makedirs('company_data')
        
        # Define the path to save the JSON file
        filepath = f'company_data/{symbol}.json'
        
        # Save the company data as JSON
        with open(filepath, 'w') as json_file:
            json.dump(company_data, json_file, indent=4)
        
        print(f"Data for {symbol} saved to {filepath}")
    else:
        print(f"No data available for {symbol}.")

# Iterate over the companies and process their data
for symbol in symbols:
    process_company_data(symbol, API_KEY)
    # Pause between API calls to avoid hitting the rate limit (5 requests per minute)
    time.sleep(12)
