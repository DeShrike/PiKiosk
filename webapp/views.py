from webapp import webapp
from flask import render_template, send_from_directory, request, redirect, url_for
from werkzeug.utils import secure_filename
from logging import getLogger
from os import listdir
from os.path import isfile, join, realpath, splitext
from .viewmodel import ViewModel
import config

STATIC_FOLDER = "./webapp/static/"

logger = getLogger(__name__)

@webapp.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static/img", "favicon.ico")

@webapp.route("/about", methods=["GET"])
def about():
    model = ViewModel()

    print(realpath('.'))

    return render_template("about.html", model = model)

@webapp.route("/", methods=["GET"])
def index():
    repository = webapp.repository
    model = ViewModel()
    model.items = [{ "index": ix, "item": item, "url": item.build_relative_url() } for (ix, item) in enumerate(repository.items) ]  

    return render_template("index.html", model = model)

@webapp.route("/uploader", methods = ["POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        filename = secure_filename(uploaded_file.filename)
        if filename != "":
            file_ext = splitext(filename)[1]
            if file_ext in webapp.config['UPLOAD_EXTENSIONS']:
                filename = join(f"{STATIC_FOLDER}{config.IMAGES_VIRTUAL_FOLDER}", filename)
                uploaded_file.save(filename)

    return redirect(url_for("new_item"))

@webapp.route("/add_url", methods=["POST"])
def add_url():

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()

    return redirect(url_for("index"))

@webapp.route("/act", methods=["POST"])
def do_action():

    if request.method == "POST":
        index = request.form.get("index")
        act = request.form.get("act")



    return redirect(url_for("index"))

@webapp.route("/add_image", methods=["POST"])
def add_image():

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()

    return redirect(url_for("index"))

@webapp.route("/new", methods=["GET"])
def new_item():
    model = ViewModel()

    staticfolder = f"{STATIC_FOLDER}{config.IMAGES_VIRTUAL_FOLDER}"
    model.available_images = sorted([f for f in listdir(staticfolder) if isfile(join(staticfolder, f))])

    return render_template("new.html", model = model)

@webapp.route("/image_centered/<image>/<bgcolor>")
def image_centered(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = f"#{bgcolor}"
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_centered.html", model = model)

@webapp.route("/image_fullscreen/<image>/<bgcolor>")
def image_fs(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = f"#{bgcolor}"
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_full_screen.html", model = model)