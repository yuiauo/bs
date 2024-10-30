import logging.config
import logging.handlers
from settings import settings


logger = logging.getLogger("bet_maker")
logging.config.dictConfig(settings.logger)
