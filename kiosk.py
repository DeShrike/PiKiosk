import json
import time
import requests
import logging
from repository import Repository
from websocket import create_connection
from config import *

logger = logging.getLogger(__name__)

class Kiosk():
    def __init__(self, repo: Repository):
        self.request_id = 0
        self.ws_url = None
        self.port = CHROMIUM_DEBUG_PORT
        self.ws_conn = self.connect_browser()
        self.must_stop = False
        self.repository = repo
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

    def send_item_to_browser(self):
        item = self.repository.items[self.repo_index]
        logger.info(f"Loading Item: {item.url}")
        if item.kind == "url":
            self.run_command("Page.navigate", url=item.url)        
        elif item.kind == "image":
            url = f"http://127.0.0.1:{PORT}"
            if item.fullscreen:
                url += "/image_fullscreen/"
            else:
                url += "/image_centered/"
            url += item.url.replace("/", "%2F")
            url += f"/{item.background_color.replace('#','')}"
            self.run_command("Page.navigate", url=url)        
        return item.duration

    def loop(self):
        self.repo_index = -1
        self.wait_duration = 10
        current_item_start_time = time.perf_counter()
        logger.info(f"Waiting {self.wait_duration} seconds")
        while not self.must_stop:
            #print(f"Waiting {self.wait_duration} seconds: {time.perf_counter() - current_item_start_time:.2f}  ")
            if time.perf_counter() - current_item_start_time > self.wait_duration:
                self.repo_index += 1
                if self.repo_index >= len(self.repository.items):
                    self.repo_index = 0
                self.wait_duration = self.send_item_to_browser()
                current_item_start_time = time.perf_counter()
                logger.info(f"Waiting {self.wait_duration} seconds")
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

