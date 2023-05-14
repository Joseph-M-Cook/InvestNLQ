import openai
import requests
import json

# OpenAI API key
openai.api_key = ""
alpha_vantage_api_key = ''


# Use Alpha Vantage API to get stock data
def get_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "GLOBAL_QUOTE"
    datatype = "json"
    
    response = requests.get(base_url, params={
        "function": function,
        "symbol": symbol,
        "apikey": alpha_vantage_api_key,
        "datatype": datatype
    }).json()

    print(response)
    return response


# Use Alpha Vantage API to get crypto data
def get_crypto_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "CURRENCY_EXCHANGE_RATE"

    response = requests.get(base_url, params={
        "function": function,
        "from_currency" : symbol,
        "to_currency": "USD",
        "apikey": alpha_vantage_api_key
    }).json()

    print(response)
    return response


# Use GPT to translate the NLQ to a symbol and call type
def extract_symbol_and_call_type(query):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": 
               "Your job is to extract the symbol of the following crypto/stock mentioned.\n"
               "You also need to determine if it is 'stock' or 'crypto'\n"
               "Respond in json with 'symbol' and 'call_type'\n"
               r'Ex: In: What is apples price today? Output:{"symbol": "AAPL","call_type": "stock"}\n'
               r'Ex: In: Bitcoin today Output:{"symbol": "BTC","call_type": "crypto"}'},
              {"role": "user", "content": query}])['choices'][0]['message']['content'].strip()
    try:
        response = json.loads(completion)
        return response['symbol'], response['call_type']
    except (json.JSONDecodeError, KeyError) as e:
        extract_symbol_and_call_type(query)


# Function to satisfy original query with retrieved data
def process_data(query, data):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0,
    messages=[{"role": "system", "content": 
               "Your job to extract all relevant data to help answer a users question.\n"
               "Do not apologize for what you are not capable of.\n"},
              {"role": "user", "content": f"Query: {query}\n"f"Data: {data}"}])['choices'][0]['message']['content'].strip()
    
    return completion


# Function to handle user input query
def handle_query(query):
    symbol, call_type = extract_symbol_and_call_type(query)

    data = ""
    # Determine call type to get data
    if call_type == 'stock':
        data = get_stock_data(symbol)

    # Determine call type to get data
    if call_type == 'crypto':
        data = get_crypto_data(symbol)
    
    response = process_data(query, data)
    return response


# Main
if __name__ == "__main__":
    query = 'What is the current price of apple?'
    print(handle_query(query))
