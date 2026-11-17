import os

# src.config loads local settings unless ENV is already set.
os.environ.setdefault("ENV", "test")
os.environ.setdefault("QUANDL_API_KEY", "test-key")
