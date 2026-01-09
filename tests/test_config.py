from viber.config import load_config, load_fabric_lakehouse_config


def test_load_config_defaults():
    config = load_config()

    assert config.environment == "development"
    assert config.log_level == "INFO"


def test_load_fabric_lakehouse_config_defaults():
    config = load_fabric_lakehouse_config()

    assert config.workspace is None
    assert config.lakehouse is None
    assert config.table is None
    assert config.path is None
    assert config.endpoint == "https://onelake.dfs.fabric.microsoft.com"
