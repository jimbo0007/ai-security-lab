import sqlite3

import pytest

from app.app import app


@pytest.fixture
def test_database(tmp_path):
    database = tmp_path / "test.db"

    db = sqlite3.connect(database)

    db.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    db.execute("""
    INSERT INTO users (id, username, email)
    VALUES (1, 'alice', 'alice@example.com')
    """)

    db.commit()
    db.close()

    return database


@pytest.fixture
def client(test_database):
    app.config["DATABASE"] = str(test_database)

    return app.test_client()


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_user_lookup(client):
    response = client.get("/user?id=1")

    assert response.status_code == 200
    assert response.json["username"] == "alice"
    assert response.json["email"] == "alice@example.com"


def test_user_lookup_rejects_invalid_id(client):
    response = client.get("/user?id=not-a-number")

    assert response.status_code == 400