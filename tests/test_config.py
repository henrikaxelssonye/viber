from viber.config import load_config


def test_load_config_defaults():
    config = load_config()

    assert config.environment == "development"
    assert config.log_level == "INFO"
