import json
import logging
import os
import shutil
import sys
from datetime import datetime, UTC
from typing import Union

from loguru import logger

from app.core.config import settings

LOG_RECORD_DEFAULT_PARAMS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
    "color_message",
}


def write_log_to_file(message: dict, logs_directory: str, filename: str) -> None:
    """
    Write logs to the specified directory and file name
    :param message: Log message to be written
    :param logs_directory: Directory for the logs folder
    :param filename: Name of the log file
    :return: None
    """
    if not os.path.exists(logs_directory):
        os.mkdir(logs_directory)

    with open(os.path.join(logs_directory, filename), 'a') as f:
        f.write(json.dumps(message) + '\n')


def create_backup(
        logs_directory: str,
        filename: str,
        max_size_in_mb: int = 10,
        max_backups: int = 3
) -> None:
    """
    Create backup after the log file reached a defined size and delete the files
    that are more the defined max backup
    :param logs_directory: Directory for the logs folder
    :param filename: Name of the log file
    :param max_size_in_mb: Size in megabytes for each log file
    :param max_backups: Number of max backups that can exist in logs folder
    :return: None
    """
    file_full_path = os.path.join(logs_directory, filename)
    file_size = os.path.getsize(file_full_path) / (1024 * 1024)

    if file_size > max_size_in_mb:
        date_now = datetime.now(UTC).replace(tzinfo=None)
        backup_filename = f"{file_full_path}_{date_now.strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy(file_full_path, backup_filename)
        backups = sorted(filter(lambda x: file_full_path in x, os.listdir()), key=os.path.getmtime, reverse=True)

        for old_backup in backups[max_backups:]:
            os.remove(old_backup)


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Propagates logs to loguru.

        :param record: record to log.
        """

        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

        if record.levelno > logging.INFO:
            detailed_log = {
                "level": record.levelname,
                "message": record.getMessage(),
                "timestamp": str(datetime.now(UTC)),
                "logger": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "thread_name": record.threadName,
                **{
                    key: value
                    for key, value in record.__dict__.items()
                    if key not in LOG_RECORD_DEFAULT_PARAMS
                }
            }
            logs_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
            filename = "log.jsonl"
            write_log_to_file(detailed_log, logs_directory, filename)
            create_backup(logs_directory, filename)


def configure_logging() -> None:
    """Configures logging."""

    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # set logs output, level and format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}</green> | "
        "<level>{level: <8}</level> | <level>{message}</level>"
    )
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level.value,
        format=log_format,
    )
