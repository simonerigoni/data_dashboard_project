from datetime import datetime
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.connectors.quandl import QuandlConnector


def test_init_requires_api_key():
    with pytest.raises(ValueError, match="API key is required"):
        QuandlConnector(None)
    with pytest.raises(ValueError, match="API key is required"):
        QuandlConnector("")


def test_get_calls_quandl_and_returns_dataframe(monkeypatch):
    raw = pd.DataFrame({"Close": [1.0, 2.0]})
    mocked = MagicMock(return_value=raw)
    monkeypatch.setattr("src.connectors.quandl.quandl.get", mocked)
    connector = QuandlConnector("secret")
    start = datetime(2018, 1, 1)
    end = datetime(2018, 1, 31)
    result = connector.get("AAPL", start, end)
    mocked.assert_called_once_with("WIKI/AAPL", start_date=start, end_date=end)
    pd.testing.assert_frame_equal(result, raw)


def test_get_table_calls_quandl(monkeypatch):
    raw = pd.DataFrame({"tot_revnu": [10]})
    mocked = MagicMock(return_value=raw)
    monkeypatch.setattr("src.connectors.quandl.quandl.get_table", mocked)
    connector = QuandlConnector("secret")
    qopts = {"columns": ["tot_revnu"]}
    result = connector.get_table("MSFT", qopts)
    mocked.assert_called_once_with("ZACKS/FC", paginate=False, ticker="MSFT", qopts=qopts)
    pd.testing.assert_frame_equal(result, raw)
