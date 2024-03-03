import logging
import sys
import io
from typing import Optional

LOG_ENTRY_DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'


def make_logger(name: str,
                file_name: Optional[str] = None,
                level: int = logging.DEBUG,
                entry_format: str = LOG_ENTRY_DEFAULT_FORMAT,
                output_stream: io.TextIOWrapper = sys.stderr
                ) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(entry_format))
        logger.addHandler(file_handler)

    if output_stream:
        stream_handler = logging.StreamHandler(output_stream)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter(entry_format))
        logger.addHandler(stream_handler)

    return logger