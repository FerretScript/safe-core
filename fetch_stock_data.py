import requests
import pandas as pd
import time

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = '87Z74N17MP35PME1'
# Stock symbol for Apple
symbol = 'AAPL'

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

            return df
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

# Retrieve time series data for the symbol
time_series_df = get_time_series_data(symbol, API_KEY)
if time_series_df is not None:
    print(f"Time Series Data for {symbol}:")
    print(time_series_df.head())

# Retrieve company overview for the symbol
company_overview = get_company_overview(symbol, API_KEY)
if company_overview is not None:
    print(f"\nCompany Overview for {symbol}:")
    for key, value in company_overview.items():
        print(f"{key}: {value}")
