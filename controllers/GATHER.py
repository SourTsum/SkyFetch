import os
import time
from datetime import datetime, timezone

from controllers import FILE
from controllers import API
from controllers import UTILS
from controllers import DISCORD

def start():
    gather_stats = FILE.get_json("data/gather_stats.json")
    current_datetime = datetime.now(timezone.utc)
    session_seconds = 0


    print("[GATHER]: Starting to gather data")
    print(f"   |Date:  {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"   |Last Ran:  {gather_stats["last_ran"]}")
    print(f"   |Seconds / Call:  {gather_stats['seconds_per_call']}\n")

    DISCORD.send_gather_start(current_datetime.strftime("%Y-%m-%d %H:%M:%S"), gather_stats)

    gather_stats["last_ran"] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    FILE.write_json(gather_stats,"../data/gather_stats.json","w")


    graph_coins_data = []
    graph_size_data = []
    running = True
    last_updated = None

    while running:
        hours = session_seconds // 3600
        minutes = (session_seconds % 3600) // 60
        seconds = session_seconds % 60

        gather_stats["session_duration"] = f"{hours:02}:{minutes:02}:{seconds:02}"



        market_data = API.get_current_market_data()
        market_data_time = datetime.fromtimestamp(market_data["lastUpdated"] / 1000)

        if session_seconds % 60 == 0 :
            clean_data = UTILS.remove_enchants(market_data)
            coins_in_market = UTILS.get_coin_circulation(clean_data)
            graph_coins_data.append(coins_in_market)
            graph_size_data.append(gather_stats["hourly_data"])

        if session_seconds != 0 and session_seconds % 180 == 0:
            UTILS.create_skyfetch_img(gather_stats,graph_coins_data,graph_size_data)
            gather_stats["hourly_data"] = 0


            # graph_coins_data.clear()
            # graph_size_data.clear()
            DISCORD.send_gather_img()

        session_seconds += gather_stats['seconds_per_call']


        print("[GATHER]:")
        print(f"   |Data Last Updated:  {market_data_time}\n")

        gather_stats["session_api_calls"] += 1
        gather_stats["hourly_api_calls"] += 1

        if last_updated  != market_data["lastUpdated"]:
            last_updated = market_data_time
            year, month, day = market_data_time.isocalendar()
            folder_path = f"output/{year}/{month}/{day}"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            mayor_data = API.get_current_mayor_data()
            del mayor_data["success"]
            del mayor_data["lastUpdated"]

            market_data.update(mayor_data)

            write_time = int(time.time())
            UTILS.write_remove_enchants(market_data,f"{folder_path}/{write_time}.json")

            data_size = FILE.compress(f"{folder_path}/{write_time}")

            gather_stats["session_data"] += round(data_size / (10 ** 9),3)
            gather_stats["hourly_data"] += round(data_size / (10 ** 6),2)

            print("[GATHER]:")
            print(f"   |Market Data logged at:  {write_time}\n")


        time.sleep(gather_stats['seconds_per_call'])