from math import sqrt

import pandas as pd
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from xgboost import XGBRegressor


def predict_with_random_forest(
    stock_df: pd.DataFrame, symbol: str, max_depth: int, n_estimators: int
) -> pd.DataFrame:
    stock_df["DATE"] = pd.to_datetime(stock_df["DATE"])
    stock_df["CLOSE"] = stock_df["CLOSE"].astype(float)
    data = (
        stock_df[["DATE", "CLOSE"]]
        .set_index(["DATE"])
        .drop_duplicates()
        .rename(columns={"CLOSE": "y"})
    )

    steps = 30
    data_train = data[:-steps]
    data_test = data[-steps:]

    regressor_RF = RandomForestRegressor(
        max_depth=max_depth, n_estimators=n_estimators, random_state=123
    )
    forecaster = ForecasterAutoreg(regressor=regressor_RF, lags=5)
    forecaster.fit(y=data_train["y"])

    predictions = forecaster.predict(steps=steps)

    error_mse = mean_squared_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    mape = mean_absolute_percentage_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    mae = mean_absolute_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    RMSE = sqrt(error_mse)

    steps = 10
    predictions_RF = forecaster.predict(steps=steps)
    fin = data_test.index.max()
    fwd_dates = pd.date_range(fin, periods=10).tolist()

    predicted = pd.DataFrame(list(zip(fwd_dates, predictions_RF)), columns=["DATE", "FORECAST"])
    predicted["mse"] = error_mse
    predicted["rmse"] = RMSE
    predicted["mape"] = mape
    predicted["mae"] = mae
    predicted["METHOD"] = "RANDOM_FOREST"
    predicted["SYMBOL"] = symbol

    return predicted


def predict_with_xgboost(
    stock_df: pd.DataFrame, symbol: str, learning_rate: float, n_estimators: int, max_depth: int
) -> pd.DataFrame:
    stock_df = stock_df[(stock_df["SYMBOL"] == "AAPL")]
    stock_df["DATE"] = pd.to_datetime(stock_df["DATE"])
    stock_df["CLOSE"] = stock_df["CLOSE"].astype(float)
    data = (
        stock_df[["DATE", "CLOSE"]]
        .set_index(["DATE"])
        .drop_duplicates()
        .rename(columns={"CLOSE": "y"})
    )

    steps = 30
    data_test = data[-steps:]

    forecaster_xgb = ForecasterAutoreg(
        regressor=XGBRegressor(
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=123,
        ),
        lags=20,
    )

    forecaster_xgb.fit(y=data["y"])
    steps = 30
    predictions = forecaster_xgb.predict(steps=steps)
    error_mse = mean_squared_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    mape = mean_absolute_percentage_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    mae = mean_absolute_error(y_true=data_test["y"][1:28], y_pred=predictions[1:28])
    RMSE = sqrt(error_mse)

    steps = 10
    predictions_XG = forecaster_xgb.predict(steps=steps)
    fin = data_test.index.max()
    fwd_dates = pd.date_range(fin, periods=10).tolist()

    predicted = pd.DataFrame(list(zip(fwd_dates, predictions_XG)), columns=["DATE", "FORECAST"])
    predicted["mse"] = error_mse
    predicted["rmse"] = RMSE
    predicted["mape"] = mape
    predicted["mae"] = mae
    predicted["METHOD"] = "XGBOOST"
    predicted["SYMBOL"] = symbol

    return predicted
