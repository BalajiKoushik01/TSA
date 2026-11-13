"""Leakage-free, one-step-ahead expanding-window seasonal-naive evaluation.

No forecasting model is fitted: this is a transparent baseline against which
trained statistical models should be compared in a separate backtest.
"""
from math import isfinite, sqrt


def rolling_seasonal_naive_rmse(prices, *, season_length=12, min_history=24):
    """Return (number_of_prior_observations, cumulative_RMSE) for each test month.

    At observation i (0-indexed), predict prices[i - season_length].
    That value is necessarily in the past. The cumulative RMSE is calculated
    from all genuine errors observed so far, with no random performance values.
    """
    if not isinstance(season_length, int) or season_length < 1:
        raise ValueError("season_length must be a positive integer")
    if not isinstance(min_history, int) or min_history < season_length:
        raise ValueError("min_history must be an integer >= season_length")
    values = [float(price) for price in prices]
    if len(values) <= min_history:
        raise ValueError("not enough observations for an out-of-sample forecast")
    if any(not isfinite(value) for value in values):
        raise ValueError("prices must contain finite values without missing months")

    history_sizes = []
    cumulative_rmse = []
    squared_error_sum = 0.0
    for index in range(min_history, len(values)):
        prediction = values[index - season_length]
        observed = values[index]
        squared_error_sum += (observed - prediction) ** 2
        history_sizes.append(index)
        cumulative_rmse.append(sqrt(squared_error_sum / (index - min_history + 1)))
    return history_sizes, cumulative_rmse
