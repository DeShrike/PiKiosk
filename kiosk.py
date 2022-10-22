import json
import time
import requests
import logging
from websocket import create_connection
from config import *

logger = logging.getLogger(__name__)

class Kiosk():
    def __init__(self):
        self.request_id = 0
        self.ws_url = None
        self.port = CHROMIUM_DEBUG_PORT
        self.ws_conn = self.connect_browser()
        self.must_stop = False
        logger.info("Connected")
        self.show_current()

    def connect_browser(self):
        logger.info("Connecting")
        sleep_step = 0.25
        wait_seconds = 10
        while wait_seconds > 0:
            try:
                url = f"http://127.0.0.1:{self.port}/json"
                resp = requests.get(url).json()
                self.ws_url = resp[0]["webSocketDebuggerUrl"]
                return create_connection(self.ws_url)
            except requests.exceptions.ConnectionError:
                logger.info("Waiting")
                time.sleep(sleep_step)
                wait_seconds -= sleep_step

        raise Exception("Unable to connect to chromium")

    def show_current(self):
        url = f"http://127.0.0.1:{self.port}/json"
        resp = requests.get(url).json()
        current_url = resp[0]["url"]
        current_title = resp[0]["title"]
        logger.info("Current Page:")
        logger.info(f"  {current_title}")
        logger.info(f"  {current_url}")

    def run_command(self, method, **kwargs):
        logger.info(f"Executing command: {method}")
        self.request_id += 1
        command = {"method": method,
                    "id": self.request_id,
                    "params": kwargs}
        self.ws_conn.send(json.dumps(command))
        while True:
            msg = json.loads(self.ws_conn.recv())
            if msg.get("id") == self.request_id:
                return msg

    def loop(self):
        while not self.must_stop:
            print("Loop")
            time.sleep(1)
    
    def stop(self):
        self.must_stop = True

def main():
    kiosk = Kiosk()
    kiosk.show_current()
    time.sleep(5)
    kiosk.run_command("Page.navigate", url="https://www.bing.com")
    time.sleep(5)
    kiosk.show_current()

if __name__ == "__main__":
    main()


#js = """
#var sel = '[role="heading"][aria-level="2"]';
#var headings = document.querySelectorAll(sel);
#headings = [].slice.call(headings).map((link)=>{return link.innerText});
#JSON.stringify(headings);
#"""
#result = run_command(conn, 'Runtime.evaluate', expression=js)
#headings = json.loads(result['result']['result']['value'])
#for heading in headings:
#    print(heading)
#browser.terminate()
