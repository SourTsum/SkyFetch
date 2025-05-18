from controllers import FILE
from controllers import DISCORD
import requests

def get_current_market_data():
    """
    requests the skyblock/bazaar API
    """
    try:
        market_data = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
        return market_data.json()
    except Exception as e:
        FILE.log_error(e)
        DISCORD.send_error("[API Controller]: Couldn't get skyblock/bazaar data")
        print("[API Controller]: Couldn't get skyblock/bazaar data")
        return None

def get_cached_market_data():
    try:
        return FILE.get_json('./output/original_market_data.json')
    except Exception as e:
        FILE.log_error(e)
        DISCORD.send_error("[API Controller]: market_data file doesn't exist OR can't read from file...")
        print("[API Controller]: market_data file doesn't exist OR can't read from file...")
        return None


def get_current_mayor_data():
    mayor_data = requests.get("https://api.hypixel.net/v2/resources/skyblock/election").json()
    return mayor_data