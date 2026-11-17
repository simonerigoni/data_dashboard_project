import pandas as pd

from dash_app import bollinger_bands


def _as_series(values) -> pd.Series:
    return pd.Series(list(values))


def test_bollinger_bands_window_and_std():
    price = pd.Series([10.0, 12.0, 14.0, 16.0, 18.0, 20.0])
    rolling_mean, upper, lower = bollinger_bands(price, window_size=3, num_of_std=1)
    mean = _as_series(rolling_mean)
    up = _as_series(upper)
    low = _as_series(lower)
    # First two values in a window of 3 are NaN
    assert mean.iloc[:2].isna().all()
    assert mean.iloc[2] == 12.0
    assert up.iloc[2] > mean.iloc[2]
    assert low.iloc[2] < mean.iloc[2]
    # Symmetric around the mean
    pd.testing.assert_series_equal((up - mean).dropna(), (mean - low).dropna(), check_names=False)


def test_bollinger_bands_constant_series_has_zero_width():
    price = pd.Series([5.0] * 12)
    rolling_mean, upper, lower = bollinger_bands(price, window_size=5, num_of_std=2)
    assert _as_series(rolling_mean).iloc[-1] == 5.0
    assert _as_series(upper).iloc[-1] == 5.0
    assert _as_series(lower).iloc[-1] == 5.0
