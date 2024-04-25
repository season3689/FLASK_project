from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config
# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

csrf = CSRFProtect()


def create_app(config_key):

    app = Flask(__name__)

    app.config.from_object( config[config_key]
        # SECRET_KEY="2asdfasdf2asdfasdf",
        # SQLALCHEMY_DATABASE_URI=
        #     f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        # SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLALCHEMY_ECHO=True,
        # WTF_CSRF_SECRET_KEY="3asdfg3asdfg3asdfg"
    )

    csrf.init_app(app)

    # SQLAlchemy와 app을 연계한다.
    db.init_app(app)

    # Migrate와 app을 연계한다.
    Migrate(app, db)


    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
