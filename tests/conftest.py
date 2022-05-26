from pathlib import Path

import pytest

from maybe_later import Config


@pytest.fixture
def base_dir() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture()
def config(base_dir: Path) -> Config:
    config_file = base_dir.joinpath("test_config.yaml")
    return Config.from_file(config_file)
