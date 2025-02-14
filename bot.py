import ccxt
import time
import requests
import json

# Load API keys from config file
with open("config.json") as config_file:
    config = json.load(config_file)

# XT.com API Setup
exchange = ccxt.xt({
    'apiKey': config["xt_api_key"],
    'secret': config["xt_api_secret"],
    'enableRateLimit': True
})

# Discord Webhook for Alerts
WEBHOOK_URL = config["discord_webhook_url"]

def send_discord_alert(message):
    """ Sends trade alerts to Discord """
    payload = {"content": message}
    requests.post(WEBHOOK_URL, json=payload)

def get_all_markets():
    """ Fetches all tradable markets on XT.com """
    try:
        markets = exchange.load_markets()
        tradable_pairs = [market for market in markets if "/USDT" in market]  # Only USDT pairs
        return tradable_pairs
    except Exception as e:
        print(f"Error fetching market list: {e}")
        return []

def get_market_data(tradable_pairs):
    """ Fetches live market prices for all tradable pairs """
    prices = {}
    for pair in tradable_pairs:
        try:
            ticker = exchange.fetch_ticker(pair)
            prices[pair] = ticker['last']
        except Exception as e:
            print(f"Error fetching {pair}: {e}")
    return prices

def analyze_market(prices):
    """ Identifies trade opportunities based on Strategies A, B, C, D """
    signals = []
    
    for pair, price in prices.items():
        if price > 50000:  # Example condition, replace with actual strategy logic
            signals.append((pair, "LONG", price))
        elif price < 40000:
            signals.append((pair, "SHORT", price))
    
    return signals

def execute_trades(signals):
    """ Executes trades based on signals """
    for pair, direction, price in signals:
        message = f"🚀 Trade Alert 🚀\n📌 **Pair:** {pair}\n📌 **Direction:** {direction}\n📌 **Entry:** {price}"
        send_discord_alert(message)
        print(message)

# Run the bot every 30 seconds
while True:
    tradable_pairs = get_all_markets()  # Get all markets dynamically
    prices = get_market_data(tradable_pairs)
    signals = analyze_market(prices)
    execute_trades(signals)
    time.sleep(30)
