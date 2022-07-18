import sqlite3
import pytest

import light_lock.sqlite_utils as utils


def test_create_table():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        assert utils.create_table(cursor, "test")
        cursor.execute("SELECT * FROM test")
        assert cursor.fetchall() == []

        assert utils.create_table(cursor, "test")  # Check no error

        assert not utils.create_table(cursor, "test-exception")  # Check exception


def test_get_lock_value():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        utils.create_table(cursor, "test")
        assert utils.get_lock_value(cursor, "test") == 0
        with pytest.raises(sqlite3.Error):
            utils.get_lock_value(cursor, "test_exception")


def test_lock_unlock():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        utils.create_table(cursor, "test")
        assert utils.get_lock_value(cursor, "test") == 0

        utils.lock(cursor, "test", "test_uuid")
        assert utils.get_lock_value(cursor, "test") == 1

        utils.unlock(cursor, "test", "test_uuid")
        assert utils.get_lock_value(cursor, "test") == 0

        utils.unlock(cursor, "test", "test_uuid")


def test_release():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        utils.create_table(cursor, "test")
        utils.lock(cursor, "test", "test_uuid1")
        utils.lock(cursor, "test", "test_uuid2")
        assert utils.get_lock_value(cursor, "test") == 2
        utils.release(cursor, "test")
        assert utils.get_lock_value(cursor, "test") == 0


def test_list_locks():
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        utils.create_table(cursor, "test")
        utils.lock(cursor, "test", "test_uuid1")
        utils.lock(cursor, "test", "test_uuid2")
        assert utils.list_locks(cursor, "test") == ["test_uuid1", "test_uuid2"]
