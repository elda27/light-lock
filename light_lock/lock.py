from datetime import datetime
from logging import getLogger
from pathlib import Path
import time
import sqlite3

from light_lock import sqlite_utils as utils
from light_lock import misc


def lock_main(
    table_name: str, count: int, file: Path, timeout: str, id: str, **kwargs
) -> int:
    if file == ":memory:":
        getLogger(__name__).error("Memory database is not supported.")
        return 1
    # Try to lock
    td_timeout = misc.to_timedelta_ext(timeout)
    start = datetime.now()
    with sqlite3.connect(
        file, timeout=td_timeout.total_seconds(), isolation_level="EXCLUSIVE"
    ) as conn:
        cursor = conn.cursor()
        if not utils.create_table(cursor, table_name):
            return 1
        lock_count = utils.get_lock_value(cursor, table_name)
        utils.lock(cursor, table_name, id)
        if lock_count < count:
            return 0  # Success

    # Wait until the lock is released
    with sqlite3.connect(
        file,
        timeout=td_timeout.total_seconds() - (datetime.now() - start).total_seconds(),
        isolation_level="DEFERRED",
    ) as conn:
        while 1:
            cursor = conn.cursor()
            utils.lock(cursor, table_name, id)

            lock_count = utils.get_lock_value(cursor, table_name)
            if lock_count < count:
                if not utils.exist_lock(cursor, table_name, id):
                    utils.lock(cursor, table_name, id)
                return 0  # Success

            time.sleep(1)

            if (datetime.now() - start) > td_timeout:
                return 1  # Error
