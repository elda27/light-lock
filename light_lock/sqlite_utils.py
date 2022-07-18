from sqlite3 import Cursor, Connection, Error
from logging import getLogger
from typing import Any, Callable, List, TypeVar
from functools import wraps


class Raise:
    pass


T = TypeVar("T")


def suppress_error(return_if_raised: Any = Raise) -> Callable[[T], T]:
    def _(func: T) -> T:
        @wraps(func)
        def __(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Error as e:
                getLogger(__name__).exception(e)
                if return_if_raised is Raise:
                    raise
                else:
                    return return_if_raised

        return __

    return _


@suppress_error(False)
def create_table(cursor: Cursor, table_name: str) -> bool:
    """Create a table in the database.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of the table.
    """
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY, uuid TEXT)"
    )
    return True


@suppress_error()
def get_lock_value(cursor: Cursor, table_name: str) -> int:
    """Get the value of the lock.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of the table.

    Returns
    -------
    int
        Value of the lock.
    """
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


@suppress_error()
def lock(cursor: Cursor, table_name: str, uuid: str) -> None:
    """Lock the semaphore.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of target table.
    uuid : str
        UUID of the lock.
    """
    if exist_lock(cursor, table_name, uuid):
        return
    cursor.execute(
        f"INSERT INTO {table_name}(uuid) VALUES(?)",
        (uuid,),
    )


@suppress_error()
def unlock(cursor: Cursor, table_name: str, uuid: str) -> None:
    """Release the semaphore.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of target table.
    uuid : str
        UUID of the lock.
    """
    cursor.execute(
        f"DELETE FROM {table_name} WHERE uuid=?",
        (uuid,),
    )


@suppress_error()
def release(cursor: Cursor, table_name: str) -> None:
    """Release the semaphore.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of target table.
    """
    cursor.execute(f"DELETE FROM {table_name}")


@suppress_error(False)
def exist_lock(cursor: Cursor, table_name: str, uuid: str) -> bool:
    """Check if the lock exists.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of target table.
    uuid : str
        UUID of the lock.

    Returns
    -------
    bool
        True if the lock exists.
    """
    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name} WHERE uuid=?",
        (uuid,),
    )
    return cursor.fetchone()[0] > 0


@suppress_error([])
def list_locks(cursor: Cursor, table_name: str) -> List[str]:
    """List of locks.

    Parameters
    ----------
    cursor : Cursor
        Cursor of the database.
    table_name : str
        Name of target table.

    Returns
    -------
    list
        List of locks.
    """
    cursor.execute(f"SELECT uuid FROM {table_name}")
    return [
        result[0]
        for result in cursor.fetchall()
    ]
