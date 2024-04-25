from pathlib import Path

basedir =Path(__file__).parent.parent

class BaseConfig:
    SECRET_KEY = "2asdf2asdf"
    WTF_CSRF_SECRET_KEY="qwer2qwer2"

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLACHEMY_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLACHEMY_ECHO = False

config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}