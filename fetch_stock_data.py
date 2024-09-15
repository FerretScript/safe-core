import requests
import pandas as pd
import time

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = '87Z74N17MP35PME1'
# Stock symbol for Apple
symbol = 'AAPL'

# Base URL for Alpha Vantage API
BASE_URL = 'https://www.alphavantage.co/query'

# Parameters for the API call
params = {
    'function': 'TIME_SERIES_DAILY',  # Retrieves daily time series data
    'symbol': symbol,
    'apikey': API_KEY,
    'outputsize': 'compact',  # 'compact' for last 100 data points; 'full' for full-length data
}

# Make the API call
response = requests.get(BASE_URL, params=params)

# Check if the request was successful
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

        # Display the first few rows
        print(df.head())
    else:
        print("Time series data not found in the response.")
else:
    print(f"Error: {response.status_code}")
