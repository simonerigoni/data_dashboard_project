# Test config
#
# python test_config.py


import src.config as conf


def test_local_env():
    assert conf.ENV == "local"
