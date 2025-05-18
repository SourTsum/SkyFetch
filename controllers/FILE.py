import json
import os
import zipfile
from pathlib import Path
from controllers import DISCORD

def write_json(response, file, mode):
    try:
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directories exist

        with file_path.open(mode, encoding="utf-8") as open_file:
            json.dump(response, open_file, ensure_ascii=False, indent=4)
    except Exception as e:
        log_error(e)
        DISCORD.send_error("[FILE Controller]: {file} file doesn't exist OR can't write to file...")
        print(f"[FILE Controller]: {file} file doesn't exist OR can't write to file...")


def write_text(response, file, mode):
    try:
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directories exist

        with file_path.open(mode, encoding="utf-8") as open_file:
            open_file.write(response)
    except Exception as e:
        log_error(e)
        DISCORD.send_error("[FILE Controller]: {file} file doesn't exist OR can't write to file...")
        print(f"[FILE Controller]: {file} file doesn't exist OR can't write to file...")


def get_json(file):
    try:
        file_path = Path(file)

        with file_path.open("r", encoding="utf-8") as open_file:
            return json.load(open_file)
    except Exception as e:
        DISCORD.send_error(str(e))
        log_error(e)
        return None

def compress(file_path):
    try:
        with zipfile.ZipFile(file_path + ".zip", "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(file_path + ".json", arcname=os.path.basename(file_path) + ".json")
        os.remove(file_path + ".json")
        return os.path.getsize(file_path + ".zip")

    except Exception as e:
        log_error(e)
        DISCORD.send_error(str(f"[FILE Controller]: {file_path}.json file couldn't be compressed..."))
        print(f"[FILE Controller]: {file_path}.json file couldn't be compressed...")



def log_error(e):
    log_file = Path("../output/logs.txt")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with log_file.open("a", encoding="utf-8") as logging:
        logging.write(str(e) + "\n")
