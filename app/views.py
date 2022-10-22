from app import app
from flask import render_template, send_from_directory
import logging
from .viewmodel import ViewModel
from config import *

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
    model.items = app.repository.items
    model.title = f"Repository {len(app.repository.items)} items"

    return render_template("index.html", model = model)

@app.route("/image_centered/<image>/<bgcolor>")
def image_centered(image: str, bgcolor: str):
    model = ViewModel()

    model.title = "Pi Kiosk"
    model.background_color = f"#{bgcolor}"
    model.image_name = IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_centered.html", model = model)

@app.route("/image_fullscreen/<image>/<bgcolor>")
def image_fs(image: str, bgcolor: str):
    model = ViewModel()

    model.title = "Pi Kiosk"
    model.background_color = f"#{bgcolor}"
    model.image_name = IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_full_screen.html", model = model)
