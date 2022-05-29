from maybe_later import Config


def test_data_folder(config: Config):
    data_folder = str(config.data_dir.absolute())
    assert data_folder.endswith("tests/data")


def test_sqlite_uri(config: Config):
    assert config.db_uri.startswith("sqlite+aiosqlite:///")
    assert config.db_uri.endswith("db.sqlite3")
