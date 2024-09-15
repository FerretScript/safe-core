import requests
import json
import time
import os

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'QKHN47GFYPCW1TNF'



# List of companies (free API symbols)
symbols = ['FDX']

# Base URL for Alpha Vantage API
BASE_URL = 'https://www.alphavantage.co/query'

# Function to retrieve income statement data
def get_income_statement(symbol, api_key):
    params = {
        'function': 'INCOME_STATEMENT',  # Retrieves income statement data
        'symbol': symbol,
        'apikey': api_key,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'annualReports' in data:
            return data['annualReports']  # Return only the annual reports part for clarity
        else:
            print(f"Income statement data not found in the response for {symbol}.")
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

    # Create a dictionary to store income statement and overview data
    company_data = {}

    # Retrieve income statement data
    income_statement_data = get_income_statement(symbol, api_key)
    if income_statement_data:
        company_data['income_statement'] = income_statement_data

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
