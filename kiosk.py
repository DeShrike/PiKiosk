import json
import time
import requests
import logging
import base64

from repository import Repository
from websocket import create_connection
import config

logger = logging.getLogger(__name__)

class KioskStatus():
    def __init__(self):
        self.product = None
        self.javascript_version = None
        self.useragent = None
        self.current_page = None

class Kiosk():
    def __init__(self, repo: Repository):
        self.request_id = 0
        self.ws_url = None
        self.port = config.CHROMIUM_DEBUG_PORT
        self.ws_conn = None
        self.must_stop = False
        self.repository = repo
        logger.info("Connected")
        self.command_running = False

    def connect_to_browser(self):
        logger.info("Connecting")
        sleep_step = 0.25
        wait_seconds = 10
        while wait_seconds > 0:
            try:
                url = f"http://127.0.0.1:{self.port}/json"
                resp = requests.get(url).json()
                self.ws_url = resp[0]["webSocketDebuggerUrl"]
                self.ws_conn = create_connection(self.ws_url)
                return
            except requests.exceptions.ConnectionError:
                logger.info("Waiting")
                time.sleep(sleep_step)
                wait_seconds -= sleep_step

        raise Exception("Unable to connect to browser")

    def get_current(self):
        url = f"http://127.0.0.1:{self.port}/json"
        resp = requests.get(url).json()
        current_url = resp[0]["url"]
        current_title = resp[0]["title"]
        return current_title, current_url

    def run_command(self, method, **kwargs):
        if self.command_running:
            return None
        if self.ws_conn is None:
            return None
        self.command_running = True
        logger.info(f"Executing command: {method}")
        self.request_id += 1
        command = {"method": method,
                    "id": self.request_id,
                    "params": kwargs}
        self.ws_conn.send(json.dumps(command))
        i = 0
        while True and i < 100:
            data = self.ws_conn.recv()
            msg = json.loads(data)
            i += 1
            # print(msg)
            if msg.get("id") == self.request_id:
                self.command_running = False
                return msg
        self.command_running = False
        return None

    def send_item_to_browser(self):
        item = self.repository.items[self.repo_index]
        logger.info(f"Loading Item: {item.url}")
        url = item.build_url()
        logger.debug(url)
        self.run_command("Page.navigate", url=url)        

        return item.duration

    def activate_by_index(self, index:int) -> None:
        self.repo_index = index - 1
        self.wait_duration = 1

    def loop(self):
        if self.ws_conn is None:
            return

        loopcounter = 0
        self.repo_index = -1
        self.wait_duration = 10
        current_item_start_time = time.perf_counter()

        logger.info(f"Waiting {self.wait_duration} seconds")
        while not self.must_stop:
            if time.perf_counter() - current_item_start_time > self.wait_duration:
                self.repo_index += 1
                if self.repo_index >= self.repository.item_count():
                    self.repo_index = 0

                self.wait_duration = self.send_item_to_browser()
                current_item_start_time = time.perf_counter()
                logger.info(f"Waiting {self.wait_duration} seconds")

            print(f"Loop {loopcounter}", end="\r")
            time.sleep(1)
            loopcounter += 1

    def execute_javascript(self):
        js = """
        var sel = '[role="heading"][aria-level="2"]';
        var headings = document.querySelectorAll(sel);
        headings = [].slice.call(headings).map((link) => { return link.innerText });
        JSON.stringify(headings);
        """
        result = self.run_command("Runtime.evaluate", expression=js)
        headings = json.loads(result['result']['result']['value'])
        for heading in headings:
            print(heading)

    def get_status(self) -> KioskStatus:
        status = KioskStatus()

        # result = self.run_command('Browser.getWindowBounds', windowId=0)

        result = self.run_command("Browser.getVersion")
        if result is not None and "result" in result and "product" in result["result"]:
            status.product = result["result"]["product"]
            status.javascript_version = result["result"]["jsVersion"]
            status.useragent = result["result"]["userAgent"]

        title, url = self.get_current()
        status.current_page = f"{title} - {url}"

        # result = self.run_command("SystemInfo.getInfo")
        # print(result)

        return status

    def get_screenshot(self):
        result = self.run_command("Page.captureScreenshot", format="png", optimizeForSpeed=True, fromSurface=False)
        if result is not None and "result" in result and "data" in result["result"]:
            data = result["result"]["data"]
            bytes = base64.b64decode(data)
            return bytes
        return None

    def stop(self):
        self.must_stop = True


def main():
    kiosk = Kiosk( Repository("r.json") )
    kiosk.connect_to_browser()
    t, u = kiosk.get_current()
    print(t, u)
    #time.sleep(5)
    #kiosk.run_command("Page.navigate", url="https://www.bing.com")
    time.sleep(5)
    #t, u = kiosk.get_current()
    #print(t, u)
    #kiosk.get_status()
    kiosk.get_screenshot()

if __name__ == "__main__":
    main()
