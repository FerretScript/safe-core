import requests
import pandas as pd
import time

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = '87Z74N17MP35PME1'

# List of companies (free API symbols)
symbols = ['AAPL', 'GOOGL', 'TSLA', 'MSFT']  # Apple, Google, Tesla, Microsoft

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

# Function to process and print data for each company
def process_company_data(symbol, api_key):
    print(f"\nProcessing data for {symbol}...")

    # Retrieve time series data
    time_series_df = get_time_series_data(symbol, api_key)
    if time_series_df is not None:
        print(f"\nTime Series Data for {symbol} (Latest 5 Days):")
        print(time_series_df.head())

    # Retrieve company overview
    company_overview = get_company_overview(symbol, api_key)
    if company_overview is not None:
        print(f"\nCompany Overview for {symbol}:")
        print(f"Market Capitalization: {company_overview.get('MarketCapitalization', 'N/A')}")
        print(f"EBITDA: {company_overview.get('EBITDA', 'N/A')}")
        print(f"PE Ratio: {company_overview.get('PERatio', 'N/A')}")
        print(f"Dividend Yield: {company_overview.get('DividendYield', 'N/A')}")
        print(f"Revenue (TTM): {company_overview.get('RevenueTTM', 'N/A')}")
        print(f"Gross Profit (TTM): {company_overview.get('GrossProfitTTM', 'N/A')}")
        print(f"Operating Margin (TTM): {company_overview.get('OperatingMarginTTM', 'N/A')}")
        
        # Highlight potential problems and insights based on this data
        print("\n--- Business Insights and Potential Issues ---")
        # Example: High PE Ratio warning
        pe_ratio = float(company_overview.get('PERatio', 0))
        if pe_ratio > 30:
            print(f"Warning: High PE Ratio ({pe_ratio}) - The stock may be overvalued.")
        else:
            print(f"PE Ratio is within a reasonable range: {pe_ratio}")

        # Example: Check for low operating margins
        operating_margin = float(company_overview.get('OperatingMarginTTM', 0))
        if operating_margin < 0.1:
            print(f"Warning: Low Operating Margin ({operating_margin}). The company may struggle with profitability.")
        else:
            print(f"Operating Margin looks healthy: {operating_margin}")

# Iterate over the companies and process their data
for symbol in symbols:
    process_company_data(symbol, API_KEY)
    # Pause between API calls to avoid hitting the rate limit (5 requests per minute)
    time.sleep(12)
