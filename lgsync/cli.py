from pathlib import Path
import argparse
from entities import Task, ConsoleArguments


def parse_args() -> ConsoleArguments:
    parser = argparse.ArgumentParser(description="LibreGarminSync CLI")
    parser.add_argument(
        "-t",
        "--transform",
        action="store_true",
        help="Transform local fit to gpx",
    )
    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="Sync remote fit to local",
    )
    parser.add_argument(
        "-o",
        "--overview_training",
        action="store_true",
        help="Run overview training task",
    )

    localPath = str(Path(__file__).resolve().parent.parent / "config.ini")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help=f"Path to the config file. Default: {localPath}",
        default=localPath,
    )

    args = parser.parse_args()
    config_file = Path(args.config)
    tasks = []

    if args.sync:
        tasks.append(Task.SYNC_REMOTE_FIT_TO_LOCAL)

    if args.transform:
        tasks.append(Task.TRANSFORM_LOCAL_FIT_TO_GPX)

    if args.overview_training:
        tasks.append(Task.Overview_TRAINING)

    return ConsoleArguments(config_file=config_file, tasks=tasks)
