import json

import pytest

import src.config as config


def test_config_constants():
    assert config.PROJECT_NAME == "data_dashboard_project"
    assert config.DATA_FOLDER == "data/"
    assert config.TICKER_FILENAME.endswith("tickers.csv")
    assert config.DEFAULT_TICKERS == ["AAPL", "MSFT"]
    assert config.DEFAULT_WINDOW_SIZE_BOLLINGER_BANDS == 10


def _patch_config_file(monkeypatch, tmp_path):
    fake_file = tmp_path / "src" / "config.py"
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    fake_file.write_text("# placeholder")
    real_abspath = config.os.path.abspath

    def fake_abspath(path):
        if path == config.__file__ or str(path).endswith("src/config.py"):
            return str(fake_file)
        return real_abspath(path)

    monkeypatch.setattr(config.os.path, "abspath", fake_abspath)


def test_load_local_settings_from_dotenv(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("EXTRA_FROM_ENV=dotenv-value\n")
    _patch_config_file(monkeypatch, tmp_path)
    config._load_local_settings()
    assert config.os.getenv("EXTRA_FROM_ENV") == "dotenv-value"


def test_load_local_settings_from_json(tmp_path, monkeypatch):
    (tmp_path / "local.settings.json").write_text(
        json.dumps({"Values": {"EXTRA_FROM_JSON": "json-value"}})
    )
    _patch_config_file(monkeypatch, tmp_path)
    config._load_local_settings()
    assert config.os.getenv("EXTRA_FROM_JSON") == "json-value"


def test_load_local_settings_missing_files_raises(tmp_path, monkeypatch):
    _patch_config_file(monkeypatch, tmp_path)
    with pytest.raises(Exception, match="Neither .env nor local.settings.json"):
        config._load_local_settings()
