from datetime import datetime, timedelta
from random import randint

from controllers import FILE
from controllers import API

import json
from PIL import Image, ImageFont, ImageDraw

def remove_enchants(market_data):
    filtered_products = {}
    for product_id, product_data in market_data["products"].items():
        if "ENCHANTMENT" not in product_id:
            filtered_products[product_id] = product_data

    return {
        "success": market_data.get("success", True),
        "lastUpdated": market_data.get("lastUpdated", 0),
        "products": filtered_products
    }



def write_remove_enchants(market_data,file_path):
    """

    :param market_data:
    :param file_path:
    :return:
    """



    FILE.write_text("{", file_path, "w")
    FILE.write_text('"success": ' + str(market_data["success"]).lower() + ",\n", file_path, "a")
    FILE.write_text('"lastUpdated": ' + str(market_data["lastUpdated"]) + ",\n", file_path, "a")
    FILE.write_text('"products": {',file_path, "a")

    market_products = market_data['products']



    first_pass = True
    for product in market_products:
        if "ENCHANTMENT" not in product:
            if first_pass:
                FILE.write_text(f'"{product}" : ' + f"{json.dumps(market_products[product])}", file_path, "a")
                first_pass = False
            else:
                FILE.write_text(",\n", file_path, "a")
                FILE.write_text(f'"{product}" : ' + f"{json.dumps(market_products[product])}", file_path, "a")

    FILE.write_text('}}', file_path, "a")

def create_skyfetch_img(gather_stats,graph_data,graph_size_data):
    font = ImageFont.truetype("arialbd.ttf", 55)
    SkyFetchIMG = Image.open("data/SkyFetch.png")
    draw = ImageDraw.Draw(SkyFetchIMG)

    x_offset , y_offset = 5250, 335
    draw_data = {
        "hourly_api_calls" : {
            "data" : str(gather_stats["hourly_api_calls"]),
            "position" : (x_offset,0 + y_offset),
        },
        "hourly_data_written" : {
            "data" : str(gather_stats["hourly_data"]) + " MB",
            "position" : (x_offset,82 + y_offset)
        },
        "session_api_calls": {
            "data" : str(gather_stats["session_api_calls"]),
            "position" : (x_offset,315 + y_offset)
        },
        "session_data_written": {
            "data" : str(gather_stats["session_data"])  + " GB",
            "position" : (x_offset,400 + y_offset)
        },
        "session_time" : {
            "data" :  str(gather_stats["session_duration"]),
            "position" : (x_offset,480 + y_offset)
        }
    }

    for i , item in enumerate(draw_data):
        draw.text(
            draw_data[item]["position"],
            draw_data[item]["data"],
            "white",
            font=font
        )

    draw_graph(draw, graph_data, 0,"orange","")
    draw_graph(draw,graph_size_data,1160,(173, 216, 230),"MB")
    SkyFetchIMG.save("output/SkyFetch.png")

def draw_point(draw, radius,x,y,color):
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

def draw_graph(draw,data, y_offset,color, tick_suffix):
    font = ImageFont.truetype("arialbd.ttf", 30)
    prev_x = None
    prev_y = None

    current = datetime.strptime("15:00", "%H:%M")

    x_pos = 4000
    while current >= datetime.strptime("14:00", "%H:%M"):
        draw.text(
            (x_pos, 1125 + y_offset),
            current.strftime("%I:%M"),
            "white",
            font=font
        )
        current -= timedelta(minutes=10)
        x_pos -= 600



    min_val = min(data)
    max_val = max(data)
    norm = [(i - min_val) / (max_val - min_val) for i in data]

    tick_count = 5
    graph_height = 800
    for i in range(tick_count):
        tick_y = y_offset + 1050 - (i * (graph_height // (tick_count - 1)))
        tick_val = min_val + (i * (max_val - min_val) / (tick_count - 1))
        tick_text = format_number(tick_val) + tick_suffix

        draw.text((290, tick_y - 15), tick_text, fill="white", font=font)

    for i in range(len(data)):


        x = 440 + 60 * i
        y = y_offset + 1050 - 800 * norm[i]

        draw_point(draw, 10, x, y,color)

        if prev_x is not None and prev_y is not None:
            draw.line((prev_x, prev_y, x, y), fill=color, width=2)

        prev_x = x
        prev_y = y

def get_coin_circulation(market_data):
    total_coin_circulation = 0

    for product_data in market_data["products"].values():
        buy_summary = product_data.get("buy_summary", [])
        quick_status = product_data.get("quick_status", {})
        total_orders = quick_status.get("buyOrders", 0)

        visible_value = 0
        visible_orders = 0
        for order in buy_summary:
            visible_value += order["amount"] * order["pricePerUnit"]
            visible_orders += order["orders"]

        if visible_orders > 0:
            estimated_value = visible_value * (total_orders / visible_orders)
            total_coin_circulation += estimated_value

    return total_coin_circulation


def format_number(val):
    abs_val = abs(val)
    if abs_val >= 1_000_000_000_000:
        return f"{val / 1_000_000_000_000:.2f}T"
    elif abs_val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f}B"
    elif abs_val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif abs_val >= 1_000:
        return f"{val / 1_000:.2f}K"
    else:
        return f"{val:.2f}"
