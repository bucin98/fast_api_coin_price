import aiologger
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.handlers.files import AsyncFileHandler
import logging


class MyFormatter(logging.Formatter):
    def format(self, record):
        return f"{record.created} - {record.name} - {record.levelname} - {record.msg}"


def setup_async_logger():
    logger = aiologger.Logger.with_default_handlers(
        name="my_app",
        level=logging.DEBUG
    )

    console_handler = AsyncStreamHandler(level=logging.DEBUG)

    file_handler = AsyncFileHandler(
        filename="my_app.log",
        mode="a",
        encoding="utf-8"
    )

    formatter = MyFormatter()

    console_handler.formatter = formatter
    file_handler.formatter = formatter

    logger.add_handler(console_handler)
    logger.add_handler(file_handler)

    return logger
