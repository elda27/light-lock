from datetime import datetime
from pathlib import Path
import sqlite3
from logging import getLogger

from light_lock import sqlite_utils as utils
from light_lock import misc


def release_main(table_name: str, file: Path, timeout: str, id: str, **kwargs) -> int:
    if file == ":memory:":
        getLogger(__name__).error("Memory database is not supported.")
        return 1
    # Try to lock
    td_timeout = misc.to_timedelta_ext(timeout)
    start = datetime.now()
    with sqlite3.connect(
        file, timeout=td_timeout.total_seconds(), isolation_level="EXCLUSIVE"
    ) as conn:
        utils.unlock(conn.cursor(), table_name, id)

    return 1 if utils.exist_lock(conn.cursor(), table_name, id) else 0
