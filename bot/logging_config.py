import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging():
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trading.log')

    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger():
    return logging.getLogger('trading_bot')


def configure_market_order_logger():
    logger = logging.getLogger('market_orders')
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'market_order.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def configure_limit_order_logger():
    logger = logging.getLogger('limit_orders')
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'limit_order.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_market_order_logger():
    return logging.getLogger('market_orders')


def get_limit_order_logger():
    return logging.getLogger('limit_orders')
