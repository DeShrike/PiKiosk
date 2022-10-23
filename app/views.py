from app import app
from flask import render_template, send_from_directory, request
import logging
from .viewmodel import ViewModel
import config

logger = logging.getLogger(__name__)

@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static/img", "favicon.ico")

@app.route("/about", methods=["GET"])
def about():
    model = ViewModel()

    return render_template("about.html", model = model)

@app.route("/", methods=["GET"])
def index():
    model = ViewModel()
    model.items = app.repository.items

    return render_template("index.html", model = model)

@app.route("/", methods=["POST"])
def index_post():

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()
    model.items = app.repository.items

    return render_template("index.html", model = model)

@app.route("/new", methods=["GET"])
def new_item():
    model = ViewModel()
    model.items = app.repository.items

    return render_template("new.html", model = model)


@app.route("/image_centered/<image>/<bgcolor>")
def image_centered(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = f"#{bgcolor}"
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_centered.html", model = model)

@app.route("/image_fullscreen/<image>/<bgcolor>")
def image_fs(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = f"#{bgcolor}"
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_full_screen.html", model = model)
