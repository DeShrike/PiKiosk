from app import app
from flask import render_template, send_from_directory
import logging
from .viewmodel import ViewModel

logger = logging.getLogger(__name__)

@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static/img", "favicon.ico")

@app.route("/about")
def about():
    model = ViewModel()
    model.title = "About"
    model.intro = "This is the 'about' text"

    return render_template("about.html", model = model)

@app.route("/")
def index():
    # logger.info("GET /")
    model = ViewModel()

    model.current_action = "(not connected)"

    return render_template("index.html", model = model)
