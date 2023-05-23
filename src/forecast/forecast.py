import sys
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import snowflake.connector
from attributes import attributes
from models import predict_with_random_forest, predict_with_xgboost
from scripts import (
    create_forecast_table,
    curated_forecast_metrics_view,
    curated_forecast_view,
    grant_forecast_metrics_view,
    grant_forecast_view,
    select_all,
)
from snowflake.connector.pandas_tools import write_pandas

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()


class Forecast:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def setup_tables(self) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(create_forecast_table)
                cursor.execute(curated_forecast_view)
                cursor.execute(curated_forecast_metrics_view)
                cursor.execute(grant_forecast_view)
                cursor.execute(grant_forecast_metrics_view)
            except Exception as e:
                raise e

    def get_current_data(self, script: str) -> None:
        """
        Pass
        """
        results = []
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(select_all)
                col_names = [x[0] for x in cursor.description]
                rows = cursor.fetchall()

                while rows:
                    results.append(rows)
                    if cursor.nextset():
                        rows = cursor.fetchall()
                    else:
                        rows = None
                results_array = np.array(results)
                results_reshaped = np.reshape(
                    results_array, (results_array.shape[1], results_array.shape[2])
                )
                self.current_data = pd.DataFrame(results_reshaped, columns=col_names)
                self.symbols = self.current_data["SYMBOL"].unique()

            except Exception as e:
                print(e)

    def get_predictions(self, attributes: Dict) -> None:
        """
        Pass
        """
        self.predictions = pd.DataFrame()

        for symbol in self.symbols:
            symbol_data = self.current_data[self.current_data["SYMBOL"] == symbol]
            symbol_attributes = attributes[symbol]
            random_forest_predictions = predict_with_random_forest(
                stock_df=symbol_data,
                symbol=symbol,
                max_depth=symbol_attributes["RANDOM_FOREST_md"],
                n_estimators=symbol_attributes["RANDOM_FOREST_ne"],
            )
            xgboost_predictions = predict_with_xgboost(
                stock_df=symbol_data,
                symbol=symbol,
                max_depth=symbol_attributes["XGB_md"],
                n_estimators=symbol_attributes["XGB_ne"],
                learning_rate=symbol_attributes["XGB_lr"],
            )
            if len(self.predictions) != 0:
                self.predictions = pd.concat(
                    [self.predictions, random_forest_predictions, xgboost_predictions]
                )
            else:
                self.predictions = pd.concat([random_forest_predictions, xgboost_predictions])

        self.predictions.columns = [col.upper() for col in self.predictions.columns]

    def upload_predictions(self, target: str) -> None:
        """
        Pass
        """
        upload_connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
            database=self.settings.DATABASE,
            schema=self.settings.PREPARED_SCHEMA,
        )
        success, nchunks, nrows, _ = write_pandas(upload_connection, self.predictions, target)
        print(success)
        print(nchunks)
        print(nrows)


if __name__ == "__main__":
    target = settings.PREPARED_FORECAST_TABLE_NAME
    settings = Settings()
    forecast = Forecast(settings)
    forecast.setup_tables()
    forecast.get_current_data(select_all)
    forecast.get_predictions(attributes)
    forecast.upload_predictions(target)
