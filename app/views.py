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

    return render_template("about.html", model = model)

@app.route("/")
def index():
    model = ViewModel()


    return render_template("index.html", model = model)

@app.route("/image_centered")
def image_centered():
    model = ViewModel()

    model.title = "sometitle"
    model.image_name = "images/testimg.jpg"

    return render_template("image_centered.html", model = model)

@app.route("/image_fullscreen")
def image_fs():
    model = ViewModel()

    model.title = "sometitle"
    model.image_name = "images/testimg.jpg"

    return render_template("image_full_screen.html", model = model)
