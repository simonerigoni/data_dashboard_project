# Config
#
# python -m src.config


import os


PROJECT_NAME = "data_dashboard_project"
DATA_FOLDER = "data/"


def _load_local_settings():
    """
    Load the local settings
    """
    import json
    from dotenv import load_dotenv

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, "../.env")
    local_settings_json_path = os.path.join(current_dir, "../local.settings.json")

    if os.path.isfile(env_path):
        load_dotenv()
    elif os.path.isfile(local_settings_json_path):
        with open(local_settings_json_path, "r") as f:
            settings = json.load(f)
        for key, value in settings["Values"].items():
            os.environ[key] = str(value)
    else:
        raise Exception(
            "Error: Neither .env nor local.settings.json was found in the project folder"
        )


if not os.getenv("ENV"):
    _load_local_settings()
else:
    pass

ENV = os.getenv("ENV")
QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")

TICKER_FILENAME = DATA_FOLDER + "tickers.csv"
INDICATOR_FILENAME = DATA_FOLDER + "indicators.csv"
DEFAULT_WINDOW_SIZE_BOLLINGER_BANDS = 10
DEFAULT_NUM_OF_STD_BOLLINGER_BANDS = 5
DEFAULT_AVAILABLE_YEARS = 5
DEFAULT_TICKERS = ["AAPL", "MSFT"]
DEFAULT_INDICATORS = ["tot_revnu", "gross_profit", "ebitda"]

if __name__ == "__main__":
    print("Config")
    print(f"{PROJECT_NAME = }")
    print(f"{ENV = }")
    print(f"{QUANDL_API_KEY = }")
else:
    pass
