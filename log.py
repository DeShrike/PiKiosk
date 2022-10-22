import logging
import logging.config

# DEBUG, INFO, WARNING, ERROR, and CRITICAL
#    Default = WARNING ----------->>>>>>

logging.config.fileConfig('logging.ini', disable_existing_loggers = False)
logger = logging.getLogger(__name__) # 'root' Logger
logger.info("Logging Initialized")

# logger.debug(__name__)
# logger.info("Hello World")
# logger.warning('Citizens of Earth, be warned!')
# logger.error("This is an error")
# logger.critical("CRIT Citizens of Earth, be warned!")
