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


utils_repository_logger = setup_logger(
    "utils_repository_logger", "utils_repository_logger.log"
)


def db_query_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        utils_repository_logger.info("The database query begins to generate")
        try:
            result = await func(*args, **kwargs)
            utils_repository_logger.info("Database query successfully completed")
            return result
        except Exception as e:
            utils_repository_logger.error(f"Database query failed: {e}")
            raise

    return wrapper
