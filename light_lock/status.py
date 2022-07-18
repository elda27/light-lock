from logging import getLogger
from pathlib import Path
import sqlite3

from light_lock import sqlite_utils as utils
from light_lock import misc


def status_main(table_name: str, file: Path, timeout: str, **kwargs):
    if file == ":memory:":
        getLogger(__name__).error("Memory database is not supported.")
        return 1
    # Try to lock
    td_timeout = misc.to_timedelta_ext(timeout)

    with sqlite3.connect(
        file,
        timeout=td_timeout.total_seconds(),
        isolation_level="DEFERRED",
    ) as conn:
        cur = conn.cursor()
        print("\n".join(utils.list_locks(cur, table_name)))
    return 0
