import argparse
from pathlib import Path
import sys
import rich


class RichArgumentParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        if message:
            if file is None:
                rich.print(message)
            else:
                file.write(message)


def main():
    parser = RichArgumentParser(
        "light_lock", description="A simple named-semaphore using sqlite3."
    )
    subparsers = parser.add_subparsers(dest="command")

    lock_parser = subparsers.add_parser(
        "lock", help="Lock a semaphore and increase a exclusive count."
    )
    release_parser = subparsers.add_parser(
        "release", help="Release a lock and decrease a exclusive count."
    )
    free_parser = subparsers.add_parser(
        "free", help="Reset a count of locked semaphore without release a semaphore."
    )
    status_parser = subparsers.add_parser(
        "status", help="Displaying try to lock semaphores"
    )
    parser.add_argument("-t", "--table-name", type=str, help="Name of the semaphore.")
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        default=Path("./.light-lock.db"),
        help="Path of the database file",
    )
    parser.add_argument(
        "--timeout", type=str, default="10s", help="Timeout of the lock."
    )

    # Lock parser
    lock_parser.add_argument(
        "-c", "--count", type=int, help="Count of the maximum exclusive lock"
    )
    lock_parser.add_argument("-i", "--id", type=str, help="ID of the lock.")

    # Status parser
    lock_parser.add_argument(
        "-t", "--table-name", type=str, help="Name of the semaphore."
    )
    lock_parser.add_argument(
        "-f",
        "--file",
        type=Path,
        default=Path("./.light-lock.db"),
        help="Path of the database file",
    )

    # Reelase parser
    release_parser.add_argument("-i", "--id", type=str, help="ID of the lock.")

    args = parser.parse_args()

    if args.command == "lock":
        from light_lock.lock import lock_main

        sys.exit(lock_main(**vars(args)))

    elif args.command == "release":
        from light_lock.release import release_main

        release_main(**vars(args))

    elif args.command == "status":
        from light_lock.status import status_main

        status_main(**vars(args))

    elif args.command == "free":
        from light_lock.free import free_main

        free_main(**vars(args))


if __name__ == "__main__":
    main()
