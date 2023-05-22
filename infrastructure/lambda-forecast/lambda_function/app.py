import sys
from pathlib import Path

from attributes import attributes
from scripts import select_all

from forecast import Forecast

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()

print("Loading function")


def lambda_handler(event, context):
    try:
        target = settings.PREPARED_FORECAST_TABLE_NAME
        forecast = Forecast(settings)
        forecast.setup_tables()
        forecast.get_current_data(select_all)
        forecast.get_predictions(attributes)
        forecast.upload_predictions(target)
        return {"forecast": "updloaded"}

    except Exception as e:
        raise e
