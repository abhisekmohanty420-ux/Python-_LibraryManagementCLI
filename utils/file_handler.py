import json
import os

FILE_PATH = "data/library.json"

def load_data():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FILE_PATH):
        return {"books": [], "users": [], "issued": []}

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid library data format.")

        for key in ("books", "users", "issued"):
            if not isinstance(data.get(key), list):
                raise ValueError(f"Invalid or missing {key} data.")

        return data

    except json.JSONDecodeError as error:
        raise ValueError("Library data file is corrupted.") from error


def save_data(data):
    os.makedirs("data", exist_ok=True)

    temp_path = FILE_PATH + ".tmp"

    with open(temp_path, "w") as file:
        json.dump(data, file, indent=4)

    os.replace(temp_path, FILE_PATH)