import pytest

from db import db
from models import UserModel, PostModel
from sqlalchemy import select


def test_db(app):
    with app.app_context():
        # UserModel.query.all()
        # PostModel.query.all()
        stmnt = select(UserModel).where(UserModel.id == 1)
        result = db.session.execute(stmnt)
        # print(f"result... {result.scalars().all()}")
        for user_obj in result.scalars():
            # print(f"{user_obj.username}")
            assert user_obj.username == "WhY S0 S3Ri0uS"

