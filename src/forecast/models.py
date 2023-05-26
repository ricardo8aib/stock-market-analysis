from math import sqrt

import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
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
    forecaster = ForecasterAutoreg(regressor=regressor_RF, lags=20)
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
    stock_df = stock_df[(stock_df["SYMBOL"] == symbol)]
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


def forecast_from_lstm(num_prediction: int, model: Sequential, n_back: int, close_data: np.array):
    forecast = close_data[-n_back:]

    for _ in range(num_prediction):
        x = forecast[-n_back:]
        x = x.reshape((1, n_back, 1))
        out = model.predict(x, verbose=0)[0][0]
        forecast = np.append(forecast, out)
    forecast = forecast[n_back - 1:]

    return forecast


def predict_with_lstm(stock_df: pd.DataFrame, symbol: str, units: int, epochs: int) -> pd.DataFrame:
    stock_df["DATE"] = pd.to_datetime(stock_df["DATE"])
    stock_df["CLOSE"] = stock_df["CLOSE"].astype(float)
    data = (
        stock_df[["DATE", "CLOSE"]]
        .set_index(["DATE"])
        .drop_duplicates()
        .rename(columns={"CLOSE": "y"})
    )

    close_data = data.to_numpy().reshape((-1, 1))
    dataindex = data.index

    steps = 30
    n_back = 3
    num_prediction = 9
    data_test = data[-steps:]

    close_train = close_data[:-steps]
    close_test = close_data[-steps:]

    train_generator = TimeseriesGenerator(close_train, close_train, length=n_back, batch_size=15)
    test_generator = TimeseriesGenerator(close_test, close_test, length=n_back, batch_size=1)

    model = Sequential()
    model.add(LSTM(units, activation="relu", input_shape=(n_back, 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")

    model.fit_generator(train_generator, epochs=epochs, verbose=None)

    prediction = model.predict_generator(test_generator)

    close_train = close_train.reshape((-1))
    close_test = close_test.reshape((-1))
    prediction = prediction.reshape((-1))

    error_mse = mean_squared_error(y_true=data_test["y"][1:28], y_pred=prediction)
    mape = mean_absolute_percentage_error(y_true=data_test["y"][1:28], y_pred=prediction)
    mae = mean_absolute_error(y_true=data_test["y"][1:28], y_pred=prediction)
    RMSE = sqrt(error_mse)

    close_data = close_data.reshape((-1))

    forecast = forecast_from_lstm(num_prediction, model, n_back, close_data)

    last_date = dataindex[-1]
    forecast_dates = pd.date_range(last_date, periods=num_prediction + 1).tolist()

    predicted = pd.DataFrame(list(zip(forecast_dates, forecast)), columns=["DATE", "FORECAST"])
    predicted["mse"] = error_mse
    predicted["rmse"] = RMSE
    predicted["mape"] = mape
    predicted["mae"] = mae
    predicted["METHOD"] = "LSTM"
    predicted["SYMBOL"] = symbol

    return predicted
