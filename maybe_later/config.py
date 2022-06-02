from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


BASEDIR = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    data_dir: Path

    @property
    def sqlite_db_path(self) -> Path:
        return self.data_dir.joinpath("db.sqlite3")

    @property
    def db_uri(self) -> str:
        sqlite_path = str(self.sqlite_db_path.absolute())
        return f"sqlite+aiosqlite:///{sqlite_path}"

    @classmethod
    def from_file(cls, config_file_path: Optional[Path] = None):
        if config_file_path is None:
            config_file_path = Path.home().joinpath(".config/maybe-later/config.yaml")
        with open(config_file_path, "r") as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)

        return cls(data_dir=Path(config_dict["paths"]["data_dir"]))
