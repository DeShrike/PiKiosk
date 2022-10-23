# TODO: Delete
from webapp import webapp
import logging

logger = logging.getLogger(__name__)

@app.route("/api/action1")
def api_action1():
    return "Action1"

@app.route("/api/action2")
def api_action2():
    return "Action2"

@app.route("/api/action3")
def api_action3():
    return "Action3"

@app.route("/api/action4")
def api_action4():
    return "Action4"

@app.route("/api/shutdown_started")
def api_shutdown_started():
    return "Shutdown Started"

@app.route("/api/shutdown_cancelled")
def api_shutdown_cancelled():
    return "Shutdown Cancelled"
