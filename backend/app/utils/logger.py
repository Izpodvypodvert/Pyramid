import functools
import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger with specified name and log file."""
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler which logs even debug messages
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)

    # Create a logging instance
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

main_logger = setup_logger(
    "main_logger", "logs/main_logger.log", level=logging.INFO
)


services_logger = setup_logger(
    "services_logger", "logs/services_logger.log", level=logging.WARNING
)

utils_repository_logger = setup_logger(
    "utils_repository_logger", "logs/utils_repository_logger.log"
)

oauth_logger = setup_logger(
    "oauth_logger", "logs/oauth_logger.log"
)


def db_query_logger(logger=utils_repository_logger):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = utils_repository_logger
            logger.info("The database query begins to generate")
            try:
                result = await func(*args, **kwargs)
                logger.info("Database query successfully completed")
                return result
            except Exception as e:
                logger.error(f"Database query failed: {e}")
                raise

        return wrapper

    return decorator
