import logging

from starlette.config import Config

logger = logging.Logger(__name__)

basic_config = Config(".env")

logger.error("basic_config.file_values.keys()")
logger.error(sorted(list(basic_config.file_values.keys())))
logger.error("basic_confic.environ.keys()")
logger.error(sorted(list(basic_config.environ.keys())))


___all__ = ["basic_config"]
