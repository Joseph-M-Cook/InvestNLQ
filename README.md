# InvestNLQ
<div align="center">
  <img src ="https://github.com/Joseph-M-Cook/InvestNLQ/blob/64f8f1038cd300a89d5a45d8f814282c14076c7e/NLQ_Logo.png"
</div>
<div align="left">
  
## Overview
InvestNLQ is an advanced financial data retrieval tool that translates natural language queries into data requests for stocks and cryptocurrencies. It uses OpenAI's GPT-4 model to interpret user queries into specific symbols and types (stock or crypto). The application fetches real-time financial data from Alpha Vantage and Finnhub APIs, serving users interested in stocks and cryptocurrencies.

## Installation
1. Clone the repository:
```
git clone https://github.com/[Joseph-M-Cook]/InvestNLQ.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Set up API keys. You need to provide your own API keys for Alpha Vantage, Finnhub, and OpenAI:
- `FINNHUB_API_KEY`
- `AV_API_KEY`
- `openai.api_key`
4. Run the script and enter your query in the command line interface:
```
python InvestNLQ.py
```
## Disclaimer
The financial data provided by this application is intended for informational purposes only. Always conduct thorough research before making investment decisions. Please use this responsibly and ensure you comply with Alpha Vantage's, Finnhub's, and OpenAI's terms of service.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
