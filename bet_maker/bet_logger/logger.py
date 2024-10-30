import logging.config


logger = logging.getLogger("BET_MAKER")

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "main",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout"]},
    },
    "filters": {}
}

logging.config.dictConfig(config=config)
logger.addHandler(logging.StreamHandler(...))
