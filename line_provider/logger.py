import logging.config
import logging.handlers
from settings import settings


logger = logging.getLogger("libe_provider")
logging.config.dictConfig(settings.logger)
