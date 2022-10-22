import log
from kiosk import Kiosk
from repository import Repository
import logging
import config
import threading
import time
import json
from config import *

kiosk = None

logger = logging.getLogger(__name__)
logger.info("Starting server")
logger.info("Initializing Flask")

from app import app

def main():
    global kiosk

    try:
        logger.info("Loading repository")
        repository = Repository(REPOSITORY_FILE)
        app.repository = repository
        logger.info("Starting Kiosk")
        kiosk = Kiosk(repository)
        x = threading.Thread(target = kiosk.loop)
        logger.info("Starting main loop")
        x.start()
        #logger.info("Starting SocketIO")
        #logger.info(f"Listening on port {config.PORT}")
        #socketio.run(app, config.HOST, config.PORT, debug = config.DEBUG, use_reloader = False)
        app.run(debug=False, port=PORT, host=HOST, use_reloader=False)
    except Exception as e:
        print(e)
        raise
    else:
        pass
    finally:
        logger.info("Stopping")
        kiosk.stop()
        time.sleep(2)

if __name__ == "__main__":
    main()
