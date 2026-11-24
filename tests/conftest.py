import pytest

from app import create_app
from config import TestConfig
from models.conn import db


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, email='student@example.com', password='password123'):
    return client.post('/register', data={
        'email': email,
        'password': password,
        'password2': password
    })


def login(client, email='student@example.com', password='password123'):
    return client.post('/login', data={
        'email': email,
        'password': password
    })