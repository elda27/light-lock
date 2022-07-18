from pathlib import Path
from tempfile import TemporaryDirectory
from light_lock.lock import lock_main
from light_lock.release import release_main
from light_lock.status import status_main
from light_lock.free import free_main
from light_lock import sqlite_utils as utils
from uuid import uuid4


def test_lock_main():
    with TemporaryDirectory() as dirname:
        main_uuid = str(uuid4()).replace("-", "_")
        sub_uuid = str(uuid4()).replace("-", "_")

        def lock(uuid) -> int:
            return lock_main("test", 1, Path(dirname) / ".light-lock.db", "1s", uuid)

        assert lock(main_uuid) == 0
        assert lock(sub_uuid) == 1


def test_status(capfd):
    with TemporaryDirectory() as dirname:
        main_uuid = str(uuid4()).replace("-", "_")
        sub_uuid = str(uuid4()).replace("-", "_")
        third_uuid = str(uuid4()).replace("-", "_")

        def lock(uuid) -> int:
            return lock_main("test", 1, Path(dirname) / ".light-lock.db", "1s", uuid)

        def unlock(uuid) -> int:
            return release_main("test", Path(dirname) / ".light-lock.db", "1s", uuid)

        def status() -> int:
            return status_main("test", Path(dirname) / ".light-lock.db", "1s")

        assert lock(main_uuid) == 0
        assert lock(sub_uuid) == 1
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == f"{main_uuid}\n{sub_uuid}\n"

        assert lock(third_uuid) == 1
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == f"{main_uuid}\n{sub_uuid}\n{third_uuid}\n"


def test_lock_unlock_main(capfd):
    with TemporaryDirectory() as dirname:
        main_uuid = str(uuid4()).replace("-", "_")
        sub_uuid = str(uuid4()).replace("-", "_")

        def lock(uuid) -> int:
            return lock_main("test", 1, Path(dirname) / ".light-lock.db", "1s", uuid)

        def unlock(uuid) -> int:
            return release_main("test", Path(dirname) / ".light-lock.db", "1s", uuid)

        def status() -> int:
            return status_main("test", Path(dirname) / ".light-lock.db", "1s")

        assert lock(main_uuid) == 0
        assert lock(sub_uuid) == 1
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == f"{main_uuid}\n{sub_uuid}\n"

        assert unlock(main_uuid) == 0
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == f"{sub_uuid}\n"


def test_free(capfd):
    with TemporaryDirectory() as dirname:
        main_uuid = str(uuid4()).replace("-", "_")
        sub_uuid = str(uuid4()).replace("-", "_")
        third_uuid = str(uuid4()).replace("-", "_")

        def lock(uuid) -> int:
            return lock_main("test", 1, Path(dirname) / ".light-lock.db", "1s", uuid)

        def free() -> int:
            return free_main("test", Path(dirname) / ".light-lock.db", "1s")

        def status() -> int:
            return status_main("test", Path(dirname) / ".light-lock.db", "1s")

        assert lock(main_uuid) == 0
        assert lock(sub_uuid) == 1
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == f"{main_uuid}\n{sub_uuid}\n"

        assert free() == 0
        assert status() == 0
        out, err = capfd.readouterr()
        assert out == "\n"
