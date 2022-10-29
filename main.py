import log
from kiosk import Kiosk
from repository import Repository
import logging
import config
import threading
import time

logger = logging.getLogger(__name__)
logger.info("Starting server")
logger.info("Initializing Flask")

from webapp import webapp

def main():
    kiosk = None
    repository = None

    try:
        logger.info("Loading repository")
        repository = Repository(config.REPOSITORY_FILE)
        
        webapp.repository = repository

        logger.info("Starting Kiosk")
        kiosk = Kiosk(repository)
        if config.ATTACH_TO_BROWSER:
            kiosk.connect_to_browser()

        webapp.kiosk = kiosk

        loop_thread = threading.Thread(target = kiosk.loop)
        logger.info("Starting main loop")
        loop_thread.start()

        webapp.run(debug=False, port=config.PORT, host=config.HOST, use_reloader=False)
    except Exception as e:
        logger.error(e)
    else:
        pass
    finally:
        logger.info("Stopping")
        kiosk.stop()
        time.sleep(2)

if __name__ == "__main__":
    main()
