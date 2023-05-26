import requests
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import openai
import json

# API Keys
FINNHUB_API_KEY = ""
AV_API_KEY = ""
openai.api_key = ""

# Use Alpha Vantage API to get stock data
def get_stock_volume(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "GLOBAL_QUOTE"
    datatype = "json"
    
    av_data = requests.get(base_url, params={
        "function": function,
        "symbol": symbol,
        "apikey": AV_API_KEY,
        "datatype": datatype
    }).json()

    if av_data and 'Global Quote' in av_data and av_data['Global Quote']:
        volume = int(av_data['Global Quote']['06. volume'])

    return volume

# Function to get current and daily stats of a stock using Finnhub
def get_stock_data(symbol):
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}')
    data = r.json()

    volume = get_stock_volume(symbol.lower())
    print(volume)

    formatted_string = f"Current price: ${data['c']}\n"\
                       f"Change: {data['d']}\n"\
                       f"Percent change: {data['dp']}%\n"\
                       f"High price of the day: ${data['h']}\n"\
                       f"Low price of the day: ${data['l']}\n"\
                       f"Open price of the day: ${data['o']}\n"\
                       f"Previous close price: ${data['pc']}"

    return formatted_string


# Use Alpha Vantage API to get crypto data
def get_crypto_current_price(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "CURRENCY_EXCHANGE_RATE"

    response = requests.get(base_url, params={
        "function": function,
        "from_currency" : symbol,
        "to_currency": "USD",
        "apikey": AV_API_KEY
    }).json()

    return float(response['Realtime Currency Exchange Rate']['5. Exchange Rate'])


# Function to get crypto data using Alpha Vantage API
def get_crypto_data(ticker):
    cc = CryptoCurrencies(key=AV_API_KEY)

    data, meta_data = cc.get_digital_currency_daily(symbol=ticker, market='USD')

    volume = [float(data[date]['5. volume']) for date in data]

    latest_date = sorted(data.keys())[-1]
    latest_data = data[latest_date]

    current_price = get_crypto_current_price(ticker)

    if latest_data:
        price_previous = float(latest_data['1a. open (USD)'])
        market_cap = latest_data['6. market cap (USD)']


        day_gain = current_price - price_previous
        day_gain_percent = (day_gain / price_previous) * 100

        volume_latest = volume[-1]
        formatted_string = f"{ticker} Trading Volume for {latest_date}: {volume_latest}\n"\
                           f"{ticker} Current Price: {current_price}\n"\
                           f"{ticker} Day Gain: {day_gain}\n"\
                           f"{ticker} Day Gain percentage: {day_gain_percent:.2f}%\n"\
                           f"{ticker} Market Cap: {market_cap}"
    else:
        formatted_string = f"Error: Could not retrieve the closing price for {latest_date}."
    print(formatted_string)
    return formatted_string


# Use GPT to translate the NLQ to a symbol and call type
def extract_symbol_and_call_type(query, count=0):
    if count == 5:
        return None, None
    
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": 
               "Your job is to extract the symbol of the following crypto/stock mentioned.\n"
               "Always assume it is a stock or crypto in question.\n"
               "You also need to determine if it is 'stock' or 'crypto'\n"
               "Respond in json with 'symbol' and 'call_type'\n"
               r'Ex: In: What is apples price today? Output:{"symbol": "AAPL","call_type": "stock"}\n'
               r'Ex: In: Bitcoin today Output:{"symbol": "BTC","call_type": "crypto"}'},
              {"role": "user", "content": query}])['choices'][0]['message']['content'].strip()
    
    try:
        response = json.loads(completion)
        return response['symbol'], response['call_type']
    except (json.JSONDecodeError, KeyError) as e:
        count += 1
        extract_symbol_and_call_type(query)


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
    
    return data

# Main
if __name__ == "__main__":

    # Testing 
    print(handle_query("What is bitcoin at"))
