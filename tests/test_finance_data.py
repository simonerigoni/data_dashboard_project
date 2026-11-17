import runpy
from unittest.mock import MagicMock

import pandas as pd

import src.connectors.quandl as quandl_module


def test_finance_data_script_prints_quandl_result(monkeypatch, capsys):
    instance = MagicMock()
    instance.get.return_value = pd.DataFrame({"Close": [1.0, 2.0]})
    mocked_cls = MagicMock(return_value=instance)
    monkeypatch.setattr(quandl_module, "QuandlConnector", mocked_cls)
    runpy.run_path("finance_data.py", run_name="__main__")
    mocked_cls.assert_called_once()
    instance.get.assert_called_once()
    out = capsys.readouterr().out
    assert "Finance data" in out
    assert "Close" in out
