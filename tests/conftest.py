import pytest

from app import create_app
from db import db
from passlib.hash import pbkdf2_sha256
from models import UserModel, PostModel
# Fixtures for the application, test client, and CLI runner
# Pytest fixtures allow writing pieces of code that are reusable across tests.
# ests are functions that start with test_, in Python modules that start with test_.
# Tests can also be further grouped in classes that start with Test.


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///data-testing.db"
    })

    # other setup can go here
    with app.app_context():
        db.init_app(app)
        db.create_all()
        seed_db(app)

    yield app
    # clean up / reset resources here
    # with app.app_context():
    #     clear_db(app)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.mark.usefixtures("app_ctx")
def seed_db(app):
    user1 = UserModel(username="WhY S0 S3Ri0uS", password=pbkdf2_sha256.hash("password"))
    db.session.add(user1)
    db.session.commit()

    post1 = PostModel(author_id=1, title="First Post!", body="this is my first post - enjoi")
    db.session.add(post1)
    db.session.commit()


@pytest.mark.usefixtures("app_ctx")
def clear_db(app):
    db.drop_all()

