import configparser
import logging


def get_logging_level(level_name: str):
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET
    }
    return levels.get(level_name)


def get_logger():
    config = configparser.ConfigParser()
    config.read("config.ini")

    log_level = config.get("logging", "level", fallback="INFO")

    logger = logging.getLogger("ANALYZER")
    logger.setLevel(get_logging_level(log_level))

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
